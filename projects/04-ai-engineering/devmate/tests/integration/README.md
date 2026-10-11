# Integration tests

Tests that need live infrastructure (Qdrant, Redis — `docker compose -f ../../../../infra/docker/docker-compose.yml up -d qdrant redis`).

Every test in here is marked `pytest.mark.integration` (registered in `pyproject.toml`). The
default run excludes integration and llm tests via `addopts = "-m 'not integration and not llm'"`;
run them explicitly with `python -m pytest -m integration -q`. CI runs this suite in the
`integration` job against Qdrant + Redis service containers.

No test in here may call a paid API. Fake the LLM boundary with a local double.
