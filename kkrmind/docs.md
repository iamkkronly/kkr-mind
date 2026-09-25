# KKR Mind — Documentation

**One API. One private AI engine. Memory. Streaming. No model names.**

Developer / Founder: কৌস্তভ কান্তি রায় (Kaustav Kanti Ray) — `@iamkkronly`

---

## Installation

```bash
pip install kkrmind
```

Or from source:

```bash
git clone https://github.com/iamkkronly/kkr-mind
cd kkr-mind
pip install -e .
```

---

## Chat

### Basic chat

```python
from kkrmind import KKRMind

ai = KKRMind()
response = ai.chat("Hello!")
print(response)
```

### Any language (Bengali, Hindi, English, ...)

```python
print(ai.chat("তুমি কে?"))
print(ai.chat("मुझे एक कहानी सुनाओ"))
```

### With a persona (system prompt)

```python
response = ai.chat(
    "hi",
    system_prompt="You are a pirate. Speak like a pirate.",
)
print(response)
```

---

## Streaming

The backend returns the complete answer in one JSON payload, so KKR Mind
streams it word-by-word on the client side for a live feel.

```python
for chunk in ai.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

With a callback:

```python
def on_token(t):
    print(t, end="", flush=True)

full = ai.chat_stream("Hello", on_chunk=on_token)
```

---

## Memory

Conversation memory is on by default. Recent turns are sent to the backend
as context (client-side, so the backend stays stateless).

```python
ai = KKRMind(memory=True, max_history=50)

ai.chat("My name is Rahul")
print(ai.chat("What is my name?"))

# Inspect / clear
print(ai.get_memory())
ai.clear_memory()
```

Disable it:

```python
ai = KKRMind(memory=False)
```

---

## Health checks

```python
report = ai.ping()
print(f"Status: {report['status']}, Latency: {report['latency_ms']}ms")
```

---

## Backend

KKR Mind talks to a single private backend API:

```
GET {API_BASE}/api
    ?chat=<your message>
    &system=<optional persona / instructions>
```

Response contract:

```json
{
  "status": "ok",
  "query": "hello",
  "response": "Hello! How can I help you today?",
  "latency_ms": 1523,
  "developer": "Kaustav Kanti Ray @iamkkronly"
}
```

The response also contains a `model` field — **KKR Mind intentionally
discards it**, so no model name is ever exposed to users.

To point the library at a different backend, change `Config.API_BASE`
and `Config.CHAT_PATH` in `kkrmind/config.py`.

---

## Errors

All errors inherit from `KKRMindError`:

| Exception | Meaning |
|---|---|
| `KKRMindError` | Base error |
| `RateLimitError` | Rate limit exceeded (retries with backoff first) |
| `NetworkError` | Backend unreachable after retries |
| `InvalidResponseError` | Backend returned an error or invalid JSON |
| `ConfigurationError` | Misconfigured client |

```python
from kkrmind import KKRMind, NetworkError, RateLimitError

ai = KKRMind(max_retries=2)
try:
    ai.chat("Hello")
except RateLimitError:
    print("Slow down a bit.")
except NetworkError as e:
    print("Backend unreachable:", e)
```

---

## Privacy

- ✅ **Local state only** — nothing stored anywhere
- ✅ **No cloud sync** — your data never leaves your machine
- ✅ **No telemetry** — zero usage tracking
- ✅ **No accounts** — no registration required
- ✅ **No model names** — the engine stays private
- ✅ **Full control** — you own all your data

---

## Examples

See the `examples/` folder in the repository:

- `examples/demo_chat.py` — basic chat
- `examples/demo_stream.py` — word-by-word streaming
- `examples/demo_memory.py` — multi-turn memory
- `examples/demo_ping.py` — health check
