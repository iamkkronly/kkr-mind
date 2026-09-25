# BUILD_GUIDE — KKR Mind কে Same-to-Same কীভাবে বানানো হয়
(How to build this kind of project, step by step)

এই গাইডে দেখানো হলো এমন একটি প্রকল্প — একটা Python AI লাইব্রেরি + নিজস্ব
private backend API — সম্পূর্ণভাবে যেভাবে বানানো, install করা, test করা
এবং PyPI-তে publish করা হয়।

This guide walks through building **KKR Mind** end-to-end: backend →
library → packaging → testing → publishing to PyPI.

---

## 0. Big picture architecture

```
┌─────────────────────┐        HTTPS (GET /api?chat=...)
│  Your Python code   │ ───────────────────────────────────┐
│  (KKRMind client)   │  ◄─────────────────────────────────│
└─────────────────────┘        JSON {status, response, ...} │
                                                                 │
                        ┌──────────────────────────────────────┐ │
                        │  Private backend API (yours)        │◄┘
                        │  - reads ?chat= and ?system=        │
                        │  - calls the AI engine (private)    │
                        │  - returns JSON (model hidden)      │
                        └──────────────────────────────────────┘
```

Key ideas:

1. **One backend endpoint** — a single API function handles all chat.
   The AI engine behind it stays 100% private (no model names).
2. **Stateless backend** — memory is handled client-side: the client
   sends the recent history inside the `system` parameter.
3. **A thin Python package** — a small, clean API (`chat`, `chat_stream`,
   `chat_with_agent`, `ping`, ...) that any Python app can `pip install`.

---

## 1. Your backend API

The backend contract (your private API — the URL itself is configured
in `kkrmind/config.py`, not shown here):

```
GET {API_BASE}/api?chat=hello%20ai
```

Response contract (this is what the client expects):

```json
{
  "status": "ok",
  "query": "hello ai",
  "response": "Hello! How can I assist you today?",
  "model": "...",            // client intentionally ignores this
  "latency_ms": 1523,
  "developer": "Kaustav Kanti Ray @iamkkronly"
}
```

If you ever rebuild it, the minimum backend code looks like this
(a plain serverless function):

```js
// backend function (any host)
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname !== "/api") {
      return new Response("Not found", { status: 404 });
    }
    const chat = url.searchParams.get("chat");
    const system = url.searchParams.get("system");
    if (!chat) {
      return Response.json({ status: "error", response: "missing ?chat=" });
    }

    const start = Date.now();
    // ... call your AI engine here (env.AI_API etc.) ...
    const response = await callYourEngine({ system, messages: [{ role: "user", content: chat }] });

    return Response.json({
      status: "ok",
      query: chat,
      response,
      latency_ms: Date.now() - start,
      developer: "Kaustav Kanti Ray @iamkkronly",
    });
  },
};
```

> Note: the current backend only reads `system` from the **query string**,
> so the Python client always uses GET with URL-encoded parameters.

---

## 2. The Python package structure

```
kkr-mind/
├── setup.py              # packaging metadata (name, version, author...)
├── setup.cfg             # egg_info options
├── requirements.txt      # runtime deps (requests)
├── MANIFEST.in           # what goes into the sdist
├── LICENSE               # MIT + upstream credit
├── README.md             # the PyPI page content (markdown)
├── kkrmind/              # the importable package
│   ├── __init__.py       # public exports + help()
│   ├── config.py         # API_BASE + settings
│   ├── exceptions.py     # KKRMindError hierarchy
│   ├── memory.py         # deque-based conversation history
│   ├── client.py         # KKRMind class — the main API
│   └── docs.md           # in-package documentation
└── examples/             # runnable demo scripts
```

Rule of thumb: **one responsibility per file**, all stateless except
`Memory`, and everything talks to the outside world through `config.py`.
That's why swapping the backend later is a one-line change.

### 2.1 `config.py` — where the backend lives

```python
class Config:
    API_BASE = "https://your-backend.example.com"   # your private API
    CHAT_PATH = "/api"
    ...
```

### 2.2 `client.py` — the core call

```python
params = {"chat": message}
if system:
    params["system"] = system
resp = self.session.get(f"{Config.API_BASE}/api", params=params, timeout=...)
data = resp.json()
if data.get("status") != "ok":
    raise InvalidResponseError(...)
return data["response"]      # data["model"] is dropped on purpose
```

Plus: retry loop with exponential backoff, memory context injection,
and word-by-word streaming.

### 2.3 `exceptions.py` — fail clearly

```python
class KKRMindError(Exception): pass
class NetworkError(KKRMindError): pass
class RateLimitError(KKRMindError): pass
...
```

Callers can catch `KKRMindError` for everything, or be specific.

---

## 3. Install & test locally

```bash
cd kkr-mind
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .

python examples/demo_ping.py      # 1) is the backend reachable?
python examples/demo_chat.py      # 2) does chat work?
python examples/demo_stream.py    # 3) streaming UX
python examples/demo_memory.py    # 4) multi-turn memory
```

In Python:

```python
import kkrmind
kkrmind.help()
```

---

## 4. Build the distributable files

```bash
pip install build twine
python -m build          # creates dist/kkrmind-1.0.0.tar.gz + .whl
twine check dist/*       # validate README renders on PyPI
```

---

## 5. Publish to PyPI

1. Create an account at <https://pypi.org/account/register/>
   - Choose a **project name** (`kkrmind`) that is not taken —
     search PyPI first.
2. Publish to **TestPyPI** first (same commands, different index):

   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ kkrmind
   ```

3. Then the real PyPI:

   ```bash
   twine upload dist/*
   ```

4. Bump the version in **two places** for every release:
   `kkrmind/__init__.py` (`__version__`) and `setup.py` (`version=`).

---

## 6. GitHub + polish (recommended)

- Push the repo to GitHub (e.g. `iamkkronly/kkr-mind`).
- Put the GitHub URL in `setup.py` (`url=` / `project_urls=`).
- Keep `README.md` as the PyPI page (it's markdown — badges, tables,
  code blocks all render).
- Add a `LICENSE` (MIT here) — always, for your own protection.

---

## 7. Checklist — "same to same" but yours

- [x] Same core as the reference library (client/config/memory/
      exceptions/docs) — slimmed down
- [x] Name: **KKR Mind** (package `kkrmind`)
- [x] Developer/Founder: **কৌস্তভ কান্তি রায় (Kaustav Kanti Ray)** `@iamkkronly`
- [x] Model names removed — one private engine, `model` field dropped
- [x] Your backend wired in (URL lives only in `kkrmind/config.py`)
- [x] Chat, memory, streaming UX, ping — all work
- [x] Agents + image generation removed (slim build)

---

## 8. Ideas for later

- **True token streaming**: make the backend stream Server-Sent Events
  (`data: {...}\n`) and parse them in `client.py` — the `chat_stream`
  signature stays identical.
- **Auth / rate limits**: add an API-key check in the backend; the client
  already handles `429` with backoff.
- **Web demo UI**: a small HTML page (or Gradio app) calling the same
  backend endpoint — the JSON contract is the same.
