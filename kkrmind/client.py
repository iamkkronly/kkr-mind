"""
KKR Mind Client - Main interface for AI interactions

Developer: Kaustav Kanti Ray (@iamkkronly)
"""

import time
from typing import Optional, Dict, Any, List, Generator

import requests

from .memory import Memory
from .exceptions import (
    KKRMindError,
    RateLimitError,
    NetworkError,
    InvalidResponseError,
)
from .config import Config


class KKRMind:
    """
    KKR Mind - one private AI engine behind one simple API

    Features:
        - Single unified AI engine (no model names exposed)
        - Memory: multi-turn conversations with context
        - Streaming-style responses (word-by-word)
        - Health checks (ping)
        - Auto-retry with exponential backoff
        - Bengali / Hindi / English / any language

    Example:
        >>> from kkrmind import KKRMind
        >>> ai = KKRMind()
        >>> print(ai.chat("Hello!"))
        'Hello! How can I help you today?'

        >>> # With memory
        >>> ai.chat("My name is Rahul")
        >>> print(ai.chat("What is my name?"))
        'Your name is Rahul.'

        >>> # Streaming style
        >>> for chunk in ai.chat_stream("Tell me a story"):
        ...     print(chunk, end="", flush=True)
    """

    def __init__(
        self,
        memory: bool = True,
        max_history: int = 50,
        auto_retry: bool = True,
        max_retries: int = 3,
        timeout: int = 120,
    ):
        """
        Initialize KKR Mind client

        Args:
            memory: Enable conversation memory (default: True)
            max_history: Max conversation history to keep (default: 50)
            auto_retry: Auto-retry on failures (default: True)
            max_retries: Max retry attempts (default: 3)
            timeout: Request timeout in seconds (default: 120)
        """
        self.config = Config()
        self.memory = Memory(max_history=max_history) if memory else None
        self.auto_retry = auto_retry
        self.max_retries = max_retries
        self.timeout = timeout

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": Config.USER_AGENT,
            "Accept": "application/json",
        })

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_system(self, system_prompt: Optional[str]) -> Optional[str]:
        """
        Build the effective system prompt.

        Combines the caller's system prompt (persona / instructions) with
        the most recent conversation history, since the backend is stateless.
        """
        parts: List[str] = []

        if system_prompt:
            parts.append(system_prompt)

        if self.memory is not None:
            history = self.memory.get_messages()[-Config.MEMORY_CONTEXT_MESSAGES:]
            if history:
                lines = [f"{m['role']}: {m['content']}" for m in history]
                parts.append(
                    "RECENT CONVERSATION (use it to keep answers coherent "
                    "and consistent with what was already said):\n"
                    + "\n".join(lines)
                )

        return "\n\n".join(parts) if parts else None

    def _request(
        self,
        message: str,
        system: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Call the KKR Mind backend with auto-retry + exponential backoff.

        The backend contract:
            GET {API_BASE}/api?chat=<message>&system=<optional persona>
            -> {"status": "ok", "query": ..., "response": ...,
                "latency_ms": ..., "developer": ...}

        Note: the backend also returns a `model` field — KKR Mind
        intentionally discards it so no model name ever reaches users.
        """
        if not message or not message.strip():
            raise KKRMindError("Message cannot be empty")

        params: Dict[str, str] = {"chat": message}
        if system:
            params["system"] = system

        last_error: Optional[Exception] = None
        attempts = self.max_retries if self.auto_retry else 1

        for attempt in range(attempts):
            try:
                start = time.time()
                resp = self.session.get(
                    Config.CHAT_ENDPOINT,
                    params=params,
                    timeout=self.timeout,
                )
                elapsed_ms = (time.time() - start) * 1000

                if resp.status_code == 429:
                    if attempt < attempts - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise RateLimitError("Rate limit exceeded")

                if resp.status_code >= 500:
                    last_error = KKRMindError(f"Backend error: {resp.status_code}")
                    if attempt < attempts - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise last_error

                if resp.status_code != 200:
                    raise KKRMindError(f"Request failed: {resp.status_code}")

                try:
                    data = resp.json()
                except ValueError:
                    raise InvalidResponseError("Backend returned invalid JSON")

                if data.get("status") != "ok" or not data.get("response"):
                    detail = data.get("response") or data.get("error") or "Unknown error"
                    raise InvalidResponseError(f"Backend error: {detail}")

                # NOTE: data.get("model") is deliberately NOT returned here.
                return {
                    "response": data["response"],
                    "latency_ms": data.get("latency_ms", round(elapsed_ms, 2)),
                    "developer": data.get("developer", Config.DEVELOPER),
                }

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_error = e
                if attempt < attempts - 1:
                    time.sleep(2 ** attempt)
                    continue

        raise NetworkError(
            f"Backend unreachable after {attempts} attempt(s): {last_error}"
        )

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Send a message to KKR Mind and get the full response.

        Args:
            message: User message
            system_prompt: Optional persona / instructions for this call

        Returns:
            str: The AI response

        Example:
            >>> ai = KKRMind()
            >>> print(ai.chat("Hello!"))
            'Hello! How can I help you today?'

            >>> # With a persona
            >>> print(ai.chat("hi", system_prompt="You are a pirate."))
        """
        system = self._build_system(system_prompt)
        result = self._request(message, system=system)

        if self.memory is not None:
            self.memory.add_message("user", message)
            self.memory.add_message("assistant", result["response"])

        return result["response"]

    def chat_stream(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        on_chunk: Optional[callable] = None,
        buffer_words: bool = False,
    ) -> Generator[str, None, str]:
        """
        Stream the response word-by-word for a fast, live feel.

        The backend returns the complete answer in one JSON payload, so
        KKR Mind chunks it word-by-word on the client side to give a
        streaming UX without buffering the whole text.

        Args:
            message: User message
            system_prompt: Optional persona / instructions
            on_chunk: Optional callback invoked with each chunk
            buffer_words: If True, yield full words (default behaviour
                          is word chunks with trailing space)

        Yields:
            Text chunks as they become available

        Returns:
            The complete response string (after the generator is exhausted)

        Example:
            >>> ai = KKRMind()
            >>> for chunk in ai.chat_stream("Tell me a story"):
            ...     print(chunk, end="", flush=True)
        """
        system = self._build_system(system_prompt)
        result = self._request(message, system=system)
        text = result["response"]

        if self.memory is not None:
            self.memory.add_message("user", message)
            self.memory.add_message("assistant", text)

        words = text.split(" ")
        word_buffer = ""
        full = ""

        for i, word in enumerate(words):
            chunk = word if (i == len(words) - 1 or buffer_words) else word + " "
            if buffer_words:
                word_buffer += chunk + (" " if i < len(words) - 1 else "")
                if i == len(words) - 1:
                    chunk = word_buffer
                    word_buffer = ""
            full += chunk
            if on_chunk is not None:
                try:
                    on_chunk(chunk)
                except Exception:
                    pass
            yield chunk

        return full

    # ------------------------------------------------------------------
    # Health checks
    # ------------------------------------------------------------------

    def ping(self) -> Dict[str, Any]:
        """
        Health check / diagnostics against the KKR Mind backend.

        Returns:
            Dict with status, latency_ms, developer, timestamp

        Example:
            >>> ai = KKRMind()
            >>> report = ai.ping()
            >>> print(report["status"], report["latency_ms"])
            ok 1523.5
        """
        report: Dict[str, Any] = {
            "status": "unknown",
            "latency_ms": None,
            "developer": Config.DEVELOPER,
            "timestamp": time.time(),
        }

        try:
            result = self._request("ping", system="Reply with just: OK")
            report["status"] = "ok"
            report["latency_ms"] = result["latency_ms"]
            report["developer"] = result["developer"]
            report["sample"] = result["response"][:60]
        except RateLimitError:
            report["status"] = "rate_limited"
        except NetworkError as e:
            report["status"] = "unreachable"
            report["error"] = str(e)
        except KKRMindError as e:
            report["status"] = "error"
            report["error"] = str(e)

        return report

    # ------------------------------------------------------------------
    # Memory + misc
    # ------------------------------------------------------------------

    def clear_memory(self):
        """Clear conversation memory."""
        if self.memory is not None:
            self.memory.clear()

    def get_memory(self) -> List[Dict[str, str]]:
        """
        Get conversation memory.

        Returns:
            List of {role, content} dicts
        """
        if self.memory is not None:
            return self.memory.get_messages()
        return []

    def __repr__(self) -> str:
        if self.memory is not None:
            return f"KKRMind(memory={len(self.memory)}/{self.memory.max_history})"
        return "KKRMind(memory=off)"
