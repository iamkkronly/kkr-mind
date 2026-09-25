# KKR Mind — Unified AI Interface

**One API. One private AI engine. Memory. Streaming. No model names.**

| | |
|---|---|
| **Developer / Founder** | কৌস্তভ কান্তি রায় (Kaustav Kanti Ray) |
| **Handle** | `@iamkkronly` |
| **License** | MIT |
| **Python** | 3.7+ |
| **Backend** | Private API |

> KKR Mind routes every request through a single private AI engine.
> No vendor names. No model IDs. Just ask, and get an answer.

---

## ✨ Features

- **One private engine** — a single unified AI behind one simple API
  (no model names are ever exposed, by design)
- **Memory** — multi-turn conversations with context
- **Streaming UX** — word-by-word responses for a live feel
- **Personas** — any system prompt per call
- **Any language** — Bengali, Hindi, English, and more
- **Health Checks** — `ping()` diagnostics with latency
- **Slim & fast** — one dependency (`requests`), ~500 lines of code
- **Privacy-First** — no storage, no cloud, no tracking

## 📦 Installation

```bash
pip install kkrmind
```

From source:

```bash
git clone https://github.com/iamkkronly/kkr-mind
cd kkr-mind
pip install -e .
```

Requirements: Python 3.7+, `requests>=2.28.0` (auto-installed).

## 🚀 Quick Start

```python
from kkrmind import KKRMind

ai = KKRMind()

# Chat
response = ai.chat("Hello!")
print(response)

# Any language
print(ai.chat("তুমি কে?"))

# With a persona
print(ai.chat("hi", system_prompt="You are a pirate."))

# Streaming (word-by-word)
for chunk in ai.chat_stream("Tell me a short story"):
    print(chunk, end="", flush=True)
```

## 🧠 Memory

```python
ai = KKRMind(memory=True, max_history=50)

ai.chat("My name is Rahul")
print(ai.chat("What is my name?"))   # -> "Your name is Rahul."

ai.clear_memory()
```

## 🩺 Health Checks

```python
report = ai.ping()
print(f"Status: {report['status']}, Latency: {report['latency_ms']}ms")
```

## 🔌 Backend

KKR Mind is built on top of a single private backend API. Every call
is a simple request:

```
GET {API_BASE}/api
    ?chat=<message>
    &system=<optional persona>
```

```json
{
  "status": "ok",
  "query": "hello",
  "response": "Hello! How can I help you today?",
  "latency_ms": 1523,
  "developer": "Kaustav Kanti Ray @iamkkronly"
}
```

The backend also reports a `model` field — **KKR Mind discards it on
purpose**, so users never see model names. To point the library at a
different backend, edit `Config.API_BASE` in `kkrmind/config.py`.

## 🔐 Privacy

- ✅ **Local state only** — nothing stored anywhere
- ✅ **No cloud sync** — data never leaves your machine
- ✅ **No telemetry** — zero usage tracking
- ✅ **No accounts** — no registration required
- ✅ **No model names** — the engine stays private
- ✅ **Full control** — you own all your data

## 📁 Project Structure

```
kkr-mind/
├── LICENSE                  # MIT (with upstream credit)
├── MANIFEST.in
├── README.md
├── requirements.txt
├── setup.py                 # PyPI packaging
├── setup.cfg
├── BUILD_GUIDE.md           # How to build & publish this project
├── kkrmind/
│   ├── __init__.py          # Public API + help()
│   ├── client.py            # KKRMind client (chat, stream, memory, ping)
│   ├── config.py            # Backend endpoint + settings
│   ├── exceptions.py        # KKRMindError hierarchy
│   ├── memory.py            # Conversation memory
│   └── docs.md              # Full in-package documentation
└── examples/
    ├── demo_chat.py
    ├── demo_stream.py
    ├── demo_memory.py
    └── demo_ping.py
```

## 🧩 Development

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
python examples/demo_chat.py
```

Full step-by-step (packaging, building the wheel, publishing to PyPI):
see [BUILD_GUIDE.md](BUILD_GUIDE.md).

## 📚 In-package docs

```python
import kkrmind
kkrmind.help()            # full docs
kkrmind.help("memory")    # one section
```

## 📄 License

MIT License — see [LICENSE](LICENSE).

## 👤 Developer

**কৌস্তভ কান্তি রায় (Kaustav Kanti Ray)** — `@iamkkronly`

**Built with ❤️ by Kaustav Kanti Ray**
