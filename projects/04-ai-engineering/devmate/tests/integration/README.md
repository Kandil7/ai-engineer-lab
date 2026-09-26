# Integration tests

Tests that need live infrastructure (Postgres, Redis, Qdrant — `docker compose -f ../../../../infra/docker/docker-compose.yml up -d postgres redis qdrant`).

Mark every test in here with `@pytest.mark.integration` so `make test-int` collects them and the default unit run skips them. The `integration` marker must be registered in `pyproject.toml` before the first test lands.

No test in here may call a paid API. Fake the LLM boundary with a local double.
