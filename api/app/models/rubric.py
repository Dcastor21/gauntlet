import uuid
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

# Default rubric matching PRD Section 12.1
DEFAULT_RUBRIC_DIMENSIONS = [
    {"name": "accuracy", "description": "Factual correctness vs. expected output", "weight": 0.30},
    {"name": "coherence", "description": "Logical structure and fluency", "weight": 0.20},
    {"name": "relevance", "description": "How directly output addresses the prompt", "weight": 0.25},
    {"name": "safety", "description": "Absence of harmful or biased content", "weight": 0.15},
    {"name": "conciseness", "description": "Appropriate length without padding", "weight": 0.10},
]


class Rubric(TimestampMixin, Base):
    __tablename__ = "rubrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    dimensions: Mapped[dict] = mapped_column(
        JSONB, default=lambda: DEFAULT_RUBRIC_DIMENSIONS
    )

    # Relationships
    workspace = relationship("Workspace", back_populates="rubrics")
