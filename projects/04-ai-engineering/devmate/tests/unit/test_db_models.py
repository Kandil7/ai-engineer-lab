"""Unit tests for the SQLAlchemy model layer.

Guards the reserved-name fix: ``metadata`` is a reserved attribute on the
SQLAlchemy Declarative API, so the models expose it as ``meta`` while keeping
the ``metadata`` column name in the database.
"""

import sqlalchemy as sa

import devmate.db as db


def test_db_module_imports_all_models():
    for name in (
        "Conversation",
        "Message",
        "EvalRun",
        "EvalResult",
        "CostRecord",
        "DocumentRecord",
    ):
        assert hasattr(db, name), f"devmate.db must export {name}"


def test_metadata_column_name_preserved_on_tables():
    for model in (db.Conversation, db.Message, db.EvalRun, db.EvalResult, db.DocumentRecord):
        assert "metadata" in model.__table__.c, f"{model.__name__} lost its metadata column"
        assert hasattr(model, "meta"), f"{model.__name__} must expose the meta attribute"


def test_metadata_column_is_jsonb():
    assert isinstance(db.Conversation.__table__.c["metadata"].type, sa.JSON)


def test_constructor_accepts_meta_kwarg():
    conv = db.Conversation(user_id="u1", title="t", meta={"k": "v"})
    assert conv.meta == {"k": "v"}
    msg = db.Message(conversation_id=None, role="user", content="hi", meta={})
    assert msg.meta == {}
