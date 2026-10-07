from sqlalchemy import Computed, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from shoe_recommender.database.models.base import Base

class CushionLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Shoe(Base):
    __tablename__ = "shoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id"),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[int | None] = mapped_column(String(100)) # could be integer, but string for weird version names

    # Physical characteristics
    weight_g: Mapped[float] = mapped_column(Float)
    heel_stack_mm: Mapped[float] = mapped_column(Float)
    forefoot_stack_mm: Mapped[float] = mapped_column(Float)
    drop_mm: Mapped[float] = mapped_column(Float, Computed("heel_stack_mm - forefoot_stack_mm"))

    # Basic categorization
    # plated: Mapped[bool | None] = mapped_column(default=False)
    # cushion: Mapped[CushionLevel | None] = mapped_column()
    use_case: Mapped[str | None] = mapped_column(String(50))
    terrain: Mapped[str | None] = mapped_column(String(50))
    
    # TODO: add responsiveness

    brand: Mapped["Brand"] = relationship(
        back_populates="shoes"
    )