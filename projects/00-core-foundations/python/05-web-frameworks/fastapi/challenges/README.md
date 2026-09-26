# FastAPI Challenge Sets

One leaf per topic, named exactly after the topic directory (see
[`../../../PRACTICE_SPEC.md`](../../../PRACTICE_SPEC.md)). Run tests from the `python/` root:

```powershell
python -m pytest 05-web-frameworks/fastapi/challenges/36-streaming-and-sse/test_challenge.py -q          # targets starter.py (fails: NotImplementedError)
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 05-web-frameworks/fastapi/challenges/36-streaming-and-sse/test_challenge.py -q          # targets solution.py (passes)
```

| Topic | Focus | Tiers |
|---|---|---|
| [36-streaming-and-sse](36-streaming-and-sse/README.md) | SSE framing, disconnect-aware token streaming, bounded backpressure | Bronze/Silver/Gold |
