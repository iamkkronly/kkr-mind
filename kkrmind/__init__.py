"""
KKR Mind - Unified AI Interface

One private AI engine behind one simple API. Chat, word-by-word
streaming, multi-turn memory, health checks — no model names ever
exposed.

Developer / Founder: কৌস্তভ কান্তি রায় (Kaustav Kanti Ray) @iamkkronly

Quick start:
    from kkrmind import KKRMind

    ai = KKRMind()

    # Standard chat
    print(ai.chat("Hello!"))

    # Streaming (word-by-word)
    for chunk in ai.chat_stream("Tell me a story"):
        print(chunk, end="", flush=True)

    # With memory
    ai.chat("My name is Rahul")
    print(ai.chat("What is my name?"))

    # Health check
    report = ai.ping()
    print(report["status"], report["latency_ms"])
"""

__version__ = "1.1.2"
__author__ = "Kaustav Kanti Ray (@iamkkronly)"

from .client import KKRMind
from .memory import Memory
from .exceptions import (
    KKRMindError,
    RateLimitError,
    NetworkError,
    InvalidResponseError,
    ConfigurationError,
)

# Documentation path
import os
_DOCS_PATH = os.path.join(os.path.dirname(__file__), "docs.md")


def get_docs():
    """Read and return the full documentation content."""
    with open(_DOCS_PATH, "r", encoding="utf-8") as f:
        return f.read()


def help(topic=None):
    """
    Print quick help or full documentation.

    Args:
        topic: Optional topic (e.g., 'chat', 'streaming', 'memory',
               'health', 'errors'). If None, prints full documentation.
    """
    if topic is None:
        print(get_docs())
        return

    docs = get_docs()
    topic_lower = topic.lower()
    lines = docs.split("\n")
    section = []
    capturing = False

    # Search ### first, then ##
    for i, line in enumerate(lines):
        if line.startswith("### ") or line.startswith("## "):
            if capturing:
                break
            if topic_lower in line.lower():
                capturing = True
                continue
        if capturing:
            section.append(line)

    if section:
        print("\n".join(section))
    else:
        print(f"Topic '{topic}' not found.")
        print("\nAvailable topics:")
        print("  - chat")
        print("  - streaming")
        print("  - memory")
        print("  - health")
        print("  - backend")
        print("  - errors")
        print("  - examples")
        print("\nUse help() without arguments for full documentation.")


__all__ = [
    "KKRMind",
    "Memory",
    "KKRMindError",
    "RateLimitError",
    "NetworkError",
    "InvalidResponseError",
    "ConfigurationError",
    "get_docs",
    "help",
]
