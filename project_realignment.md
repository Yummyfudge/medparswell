*** Begin Patch
*** Update File: project_realignment.md
+Below is a **deliberately opinionated, end‑to‑end roadmap** that should get you from “nothing works and I see no logs” to a stable, test‑driven loop that is easy to reason about and difficult to break.  It does **not** ask you to rewrite everything today—but it does give you a clear north‑star design, plus incremental checkpoints you can tackle one by one.
+
+---
+
+## 1  Make the problem visible: observability first
+### 1.1  Use a real logging config instead of shell redirection  
+Redirection (`> logs/server.log 2>&1`) captures stdout/stderr **after** Uvicorn’s own handlers format it, which often swallows useful context.  Add a `logging.yml` beside `app/main.py` and teach Uvicorn to load it:
+
+```bash
+uvicorn app.main:app \
+  --host 0.0.0.0 --port 8000 \
+  --log-config logging.yml \
+  --reload
+```
+
+Example `logging.yml` (YAML keeps it readable):
+
+```yaml
+version: 1
+disable_existing_loggers: false
+
+formatters:
+  default:
+    format: '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
+    datefmt: '%Y-%m-%dT%H:%M:%SZ'
+
+handlers:
+  console:
+    class: logging.StreamHandler
+    formatter: default
+  file:
+    class: logging.handlers.RotatingFileHandler
+    formatter: default
+    filename: logs/server.log
+    maxBytes: 10_485_760   # 10 MiB
+    backupCount: 3
+
+root:
+  level: INFO
+  handlers: [console, file]
+```
+
+*Why this matters:*  
+- You can raise the **root level to DEBUG** temporarily from the CLI.  
+- Tracebacks are preserved with timestamps.  
+- Log rotation stops runaway files on long‑running boxes.
+
+### 1.2  Log the exact CLI call and its outputs  
+Wrap your shell‑out logic in a tiny adapter class (we’ll formalize this in §3):
+
+```python
+class LlamaCLI:
+    def __init__(self, binary: Path):
+        self.binary = binary
+
+    async def run(self, prompt: str, max_tokens: int) -> str:
+        cmd = [str(self.binary), "--prompt", prompt, "--n-predict", str(max_tokens)]
+        logger.debug("Executing %s", " ".join(shlex.quote(c) for c in cmd))
+        proc = await asyncio.create_subprocess_exec(
+            *cmd,
+            stdout=asyncio.subprocess.PIPE,
+            stderr=asyncio.subprocess.PIPE,
+        )
+        out, err = await proc.communicate()
+        logger.debug("llama-cli stdout: %s", out.decode()[:500])
+        if err:
+            logger.warning("llama-cli stderr: %s", err.decode())
+        if proc.returncode:
+            raise RuntimeError(f"llama-cli exited with {proc.returncode}")
+        return out.decode()
+```
+
+Now every failure surface is in the **same** log stream.
+
+---
+
+## 2  Unblock your local TDD loop
+
+### 2.1  Fix the FastAPI test client scope issue once  
+Pytest + FastAPI + async fixtures can fight each other.  Use this canonical pattern (no plug‑ins required):
+
+```python
+import pytest
+from httpx import AsyncClient
+from app.main import app   # import AFTER app has dependencies wired
+
+@pytest.fixture
+def anyio_backend():
+    return "asyncio"
+
+@pytest.mark.anyio
+async def test_ping_works():
+    async with AsyncClient(app=app, base_url="http://test") as ac:
+        r = await ac.get("/ping")
+    assert r.json() == {"message": "pong"}
+```
+
+If you need to override dependencies (e.g., inject a fake `LlamaCLI`), do it through `app.dependency_overrides` *inside the test* and revert afterwards:
+
+```python
+@pytest.mark.anyio
+async def test_summarize_fake(monkeypatch):
+    async def _fake_llama(prompt: str, max_tokens: int):
+        return "fake answer"
+
+    app.dependency_overrides[get_llama_cli] = lambda: _fake_llama
+    async with AsyncClient(app=app, base_url="http://test") as ac:
+        r = await ac.post("/summarize", json={"prompt": "hi"})
+    assert r.status_code == 200
+    assert r.json()["summary"] == "fake answer"
+    app.dependency_overrides.clear()
+```
+
+### 2.2  Stop fighting Pydantic naming mismatches  
+Pick one and freeze it.  A common, self‑documenting choice:
+
+```python
+class SummarizeRequest(BaseModel):
+    prompt: constr(min_length=1, strip_whitespace=True)
+    max_tokens: PositiveInt = Field(alias="max_tokens", default=128)
+    # Accept ctx_size for backward‑compatibility, but mark it deprecated
+    ctx_size: Optional[int] = Field(None, deprecated=True)
+
+    model_config = ConfigDict(populate_by_name=True, extra="forbid")
+```
+
+Tests should send `max_tokens`.  If old clients still hit `ctx_size`, raise a 422 with an explicit error message.
+
+---
+
+## 3  Establish a thin, test‑friendly service boundary
+
+```
+            FastAPI route
+                  │
+          ┌───────┴────────┐            (pure-Python)
+          │ SummarizeService│  <───── dependency override in tests
+          └───────┬────────┘
+                  │
+          (async call boundary)
+                  │
+          ┌───────┴────────┐            (external)
+          │   LlamaCLI     │  <───── fake binary or monkeypatch
+          └────────────────┘
+```
+
+*Key properties*  
+
+1. **Outside world** is *only* `LlamaCLI`.  
+2. Everything above it is ordinary Python you can unit‑test with zero shelling.  
+3. Real vs fake CLI is decided at **dependency‑injection time**, not through `if DEBUG` flags.
+
+---
+
+## 4  Reconnect fake vs real CLI confidently
+
+| What you test | Substitute |
+|---------------|------------|
+| Unit tests on `SummarizeService` | an `async lambda` that returns deterministic text |
+| Route tests (`/summarize`) | override dependency to same fake |
+| Contract test of adapter | invoke the **real compiled** `llama-cli` once in CI (mark as `slow`) |
+| Local dev on Mac | fake binary in `tests/fakes/bin` on `$PATH` |
+| Linux box | real `llama-cli` on `$PATH`, plus an integration‑test script that calls it directly and asserts exit code 0 |
+
+Because the adapter logs the **exact command**, you will immediately know when `$PATH` is wrong or the binary crashes.
+
+---
+
+## 5  Lock the directory & naming policy to stop churn
+
+**Rule:** *If a file exposes one public concept, its name is that concept.*  
+- `schemas/summarize.py` (Pydantic models)  
+- `services/summarize.py` (business logic)  
+- `routes/summarize.py` (FastAPI APIRouter)  
+
+Anything else (helpers, factories) goes under `internal/` so IDE auto‑imports never collide with public module names.  **Freeze this mapping in `CONTRIBUTING.md`**—tests should fail if someone breaks it.
+
+---
+
+## 6  Decide (now, not later) whether subprocess is still OK
+
+Shelling out is fine **today** if:  
+
+- You only need one‑shot, batch‑style inference.  
+- Latency is not critical (cold binary start).  
+- You cannot risk C++ bindings in prod yet.
+
+But `llama.cpp` **does** ship a C API (`llama_eval`, etc.) that can be wrapped with `ctypes` or `pybind11`.  Moving there later will:  
+
+- Remove the IO/encoding headaches.  
+- Let you stream tokens back to the client (SSE / websockets).  
+- Simplify resource cleanup on shutdown.
+
+Put a **“migration note”** in the README so everyone knows it is future work—not a surprise refactor at 02:00.
+
+---
+
+## 7  Practical next steps (one pomodoro each)
+
+1. **Add `logging.yml`;** run on Linux box and confirm crash stack traces now appear.  
+2. **Introduce `LlamaCLI` adapter** (copy/paste above).  Commit.  
+3. **Refactor tests** into three layers (unit / route / adapter).  Get green locally with fake CLI.  
+4. **Push to Linux**; run `pytest -m "not slow"`—these should stay green.  
+5. **Write one `slow` test** that calls the real binary on the server; mark it xfail if binary missing so CI still passes on Mac.  
+6. **Document naming convention** and merge.
+
+At that point you will (a) see every failure in a single log, (b) crash early if the CLI path is wrong, and (c) have a reliable green‑red‑refactor loop again.
+
+---
+
+### Final takeaway
+
+You don’t have a *hard* bug; you have **missing feedback** and **fluid boundaries**.  Put walls around the shell process, surface its stdout/stderr, and freeze your public module names.  Once the noise stops, the remaining issues will shrink to normal‑sized pull‑requests instead of day‑long rabbit holes.
+
+Good luck—and remember to `git commit -m "Working logging + stable tests 🚀"` once you get the first green run!
+
*** End Patch