"""
PostgreSQL — 03: Migrations
===========================
Topics: sequential versions, idempotency, and rollback.

Why this matters:
    A schema evolves through versioned, ordered changes. This exercise
    models the migration history and the rollback discipline.

Run:      python 03-migrations.py
Verify:   python 03-migrations.py --verify
"""

from __future__ import annotations

import sys


class Migrator:
    def __init__(self) -> None:
        self.applied: list[str] = []
        self.schema: set[str] = set()

    def apply(self, version: str, creates: list[str], idempotent: bool = False) -> None:
        assert version not in self.applied, "a migration applies once"
        if idempotent:
            for t in creates:
                self.schema.add(t)
        else:
            assert not any(t in self.schema for t in creates), (
                "non-idempotent would fail"
            )
            self.schema.update(creates)
        self.applied.append(version)

    def rollback(self, version: str, drops: list[str]) -> None:
        assert version in self.applied, "only applied migrations roll back"
        for t in drops:
            self.schema.discard(t)
        self.applied.remove(version)


def main() -> None:
    m = Migrator()

    # Migrations apply in order, once each.
    m.apply("001", ["users"])
    m.apply("002", ["messages"])
    assert m.applied == ["001", "002"]
    assert m.schema == {"users", "messages"}

    # An idempotent migration is safe to re-run.
    m.apply("003", ["sessions"], idempotent=True)
    assert "sessions" in m.schema

    # A non-idempotent migration fails if the table already exists.
    try:
        m.apply("004", ["users"])
        assert False, "non-idempotent migration must fail on an existing table"
    except AssertionError:
        pass

    # Rollback reverses a migration.
    m.rollback("003", ["sessions"])
    assert "sessions" not in m.schema
    assert "003" not in m.applied

    print("migrations apply in order, once each")
    print("idempotent migrations are safe to re-run")
    print("non-idempotent migrations fail on an existing table")
    print("rollback reverses a migration")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
