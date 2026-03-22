import uuid
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[str] = mapped_column(
        Text, nullable=False, index=True
    )  # Clerk user ID
    plan: Mapped[str] = mapped_column(
        String(20), default="free"
    )  # free | pro | enterprise

    # Relationships
    eval_runs = relationship("EvalRun", back_populates="workspace", lazy="selectin")
    test_sets = relationship("TestSet", back_populates="workspace", lazy="selectin")
    rubrics = relationship("Rubric", back_populates="workspace", lazy="selectin")
