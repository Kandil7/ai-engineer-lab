"""
Database models and connection management.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from devmate.config import settings


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Conversation(Base):
    """Conversation/session model."""

    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata", default=dict)

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
    eval_runs: Mapped[list["EvalRun"]] = relationship(
        "EvalRun", back_populates="conversation", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_conversations_user_created", "user_id", "created_at"),)


class Message(Base):
    """Message within a conversation."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # user, assistant, system, tool
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata", default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")

    __table_args__ = (Index("ix_messages_conversation_created", "conversation_id", "created_at"),)


class EvalRun(Base):
    """Evaluation run record."""

    __tablename__ = "eval_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dataset: Mapped[str] = mapped_column(String(255), nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )  # pending, running, completed, failed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata", default=dict)

    # Relationships
    conversation: Mapped[Optional["Conversation"]] = relationship(
        "Conversation", back_populates="eval_runs"
    )
    eval_results: Mapped[list["EvalResult"]] = relationship(
        "EvalResult", back_populates="eval_run", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_eval_runs_dataset_started", "dataset", "started_at"),)


class EvalResult(Base):
    """Individual evaluation result."""

    __tablename__ = "eval_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    eval_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("eval_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    ground_truth: Mapped[str | None] = mapped_column(Text, nullable=True)
    contexts: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)
    scores: Mapped[dict[str, float]] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata", default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    eval_run: Mapped["EvalRun"] = relationship("EvalRun", back_populates="eval_results")


class CostRecord(Base):
    """Cost tracking record."""

    __tablename__ = "cost_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_cost_records_provider_model_created", "provider", "model", "created_at"),
        Index("ix_cost_records_created", "created_at"),
    )


class DocumentRecord(Base):
    """Indexed document record."""

    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    chunk_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata", default=dict)
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("source", "chunk_index", name="uq_document_source_chunk"),
        Index("ix_documents_filename", "filename"),
    )


# Database connection
engine = None
async_session_factory = None


async def init_db() -> None:
    """Initialize database connection and create tables."""
    global engine, async_session_factory

    engine = create_async_engine(
        settings.postgres_connection_url,
        echo=settings.debug,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )

    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Get database session (for FastAPI dependency)."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_db() -> None:
    """Close database connection."""
    global engine
    if engine:
        await engine.dispose()


# Repository classes for common operations
class ConversationRepository:
    """Conversation data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, user_id: str = None, title: str = None, metadata: dict = None
    ) -> Conversation:
        conv = Conversation(user_id=user_id, title=title, meta=metadata or {})
        self.session.add(conv)
        await self.session.flush()
        return conv

    async def get(self, conv_id: uuid.UUID) -> Conversation | None:
        result = await self.session.execute(select(Conversation).where(Conversation.id == conv_id))
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> list[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def update_title(self, conv_id: uuid.UUID, title: str) -> bool:
        conv = await self.get(conv_id)
        if conv:
            conv.title = title
            return True
        return False

    async def delete(self, conv_id: uuid.UUID) -> bool:
        conv = await self.get(conv_id)
        if conv:
            await self.session.delete(conv)
            return True
        return False


class MessageRepository:
    """Message data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        token_count: int = None,
        model: str = None,
        latency_ms: float = None,
        cost_usd: float = None,
        metadata: dict = None,
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            token_count=token_count,
            model=model,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            meta=metadata or {},
        )
        self.session.add(msg)
        await self.session.flush()
        return msg

    async def get_conversation_messages(
        self,
        conversation_id: uuid.UUID,
        limit: int = 100,
    ) -> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())


class CostRepository:
    """Cost data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def record(self, record: CostRecord) -> CostRecord:
        self.session.add(record)
        await self.session.flush()
        return record

    async def get_summary(
        self,
        since: datetime = None,
        provider: str = None,
        model: str = None,
    ) -> dict[str, Any]:
        query = select(CostRecord)

        if since:
            query = query.where(CostRecord.created_at >= since)
        if provider:
            query = query.where(CostRecord.provider == provider)
        if model:
            query = query.where(CostRecord.model == model)

        result = await self.session.execute(query)
        records = list(result.scalars().all())

        # Aggregate
        total_requests = len(records)
        total_tokens = sum(r.total_tokens for r in records)
        total_cost = sum(r.cost_usd for r in records)
        total_latency = sum(r.latency_ms for r in records)

        by_model = {}
        by_provider = {}

        for r in records:
            if r.model not in by_model:
                by_model[r.model] = {"requests": 0, "tokens": 0, "cost": 0.0, "latency_ms": 0.0}
            by_model[r.model]["requests"] += 1
            by_model[r.model]["tokens"] += r.total_tokens
            by_model[r.model]["cost"] += r.cost_usd
            by_model[r.model]["latency_ms"] += r.latency_ms

            if r.provider not in by_provider:
                by_provider[r.provider] = {
                    "requests": 0,
                    "tokens": 0,
                    "cost": 0.0,
                    "latency_ms": 0.0,
                }
            by_provider[r.provider]["requests"] += 1
            by_provider[r.provider]["tokens"] += r.total_tokens
            by_provider[r.provider]["cost"] += r.cost_usd
            by_provider[r.provider]["latency_ms"] += r.latency_ms

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "avg_latency_ms": total_latency / max(total_requests, 1),
            "by_model": by_model,
            "by_provider": by_provider,
        }


class EvalRepository:
    """Evaluation data access."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_run(
        self,
        name: str,
        dataset: str,
        conversation_id: uuid.UUID = None,
        metadata: dict = None,
    ) -> EvalRun:
        run = EvalRun(
            name=name,
            dataset=dataset,
            conversation_id=conversation_id,
            meta=metadata or {},
        )
        self.session.add(run)
        await self.session.flush()
        return run

    async def add_result(
        self,
        eval_run_id: uuid.UUID,
        question: str,
        answer: str,
        ground_truth: str = None,
        contexts: list[dict] = None,
        scores: dict[str, float] = None,
        latency_ms: float = None,
        cost_usd: float = None,
        metadata: dict = None,
    ) -> EvalResult:
        result = EvalResult(
            eval_run_id=eval_run_id,
            question=question,
            answer=answer,
            ground_truth=ground_truth,
            contexts=contexts or [],
            scores=scores or {},
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            meta=metadata or {},
        )
        self.session.add(result)
        await self.session.flush()
        return result

    async def complete_run(self, eval_run_id: uuid.UUID, metrics: dict[str, Any]) -> None:
        run = await self.session.get(EvalRun, eval_run_id)
        if run:
            run.status = "completed"
            run.completed_at = datetime.now(UTC)
            run.metrics = metrics
