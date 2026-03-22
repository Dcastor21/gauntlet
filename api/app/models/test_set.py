import uuid
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TestSet(TimestampMixin, Base):
    __tablename__ = "test_sets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    task_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # generation | classification | rag | code
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text), default=list)
    task_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    workspace = relationship("Workspace", back_populates="test_sets")
    tasks = relationship("TestTask", back_populates="test_set", lazy="selectin")


class TestTask(Base):
    __tablename__ = "test_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    test_set_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("test_sets.id"), nullable=False, index=True
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)  # For RAG tasks
    metadata: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    # Relationships
    test_set = relationship("TestSet", back_populates="tasks")
