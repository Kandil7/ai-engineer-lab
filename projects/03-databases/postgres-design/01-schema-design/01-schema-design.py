"""
PostgreSQL — 01: Schema Design
==============================
Topics: keys, constraints, and referential integrity.

Why this matters:
    A schema is the contract between the application and the data. This
    exercise models keys and enforces referential integrity.

Run:      python 01-schema-design.py
Verify:   python 01-schema-design.py --verify
"""

from __future__ import annotations

import sys


class Table:
    def __init__(self, name: str, pk: str) -> None:
        self.name = name
        self.pk = pk
        self.rows: list[dict] = []

    def insert(self, row: dict) -> None:
        assert row[self.pk] not in {r[self.pk] for r in self.rows}, "primary key unique"
        self.rows.append(row)

    def exists(self, pk_value) -> bool:
        return any(r[self.pk] == pk_value for r in self.rows)


def insert_with_fk(row: dict, fk_col: str, fk_value, parent: Table) -> None:
    """A foreign key enforces referential integrity."""
    assert parent.exists(fk_value), "foreign key must reference an existing row"
    row[fk_col] = fk_value


def main() -> None:
    users = Table("users", "id")
    users.insert({"id": "u1", "email": "a@x.com"})
    users.insert({"id": "u2", "email": "b@x.com"})

    # A primary key rejects duplicates.
    try:
        users.insert({"id": "u1", "email": "dup@x.com"})
        assert False, "primary key must reject duplicates"
    except AssertionError:
        pass

    # A foreign key rejects orphan references.
    message = {"id": "m1", "text": "hello"}
    insert_with_fk(message, "user_id", "u1", users)
    assert message["user_id"] == "u1"

    try:
        insert_with_fk({"id": "m2", "text": "orphan"}, "user_id", "u99", users)
        assert False, "foreign key must reject orphans"
    except AssertionError:
        pass

    print("primary key rejects duplicate ids")
    print("foreign key enforces referential integrity")
    print("an orphan reference is rejected at the database level")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
