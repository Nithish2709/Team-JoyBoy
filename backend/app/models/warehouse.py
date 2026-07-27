"""
Warehouse model — PDS grain storage facilities.
"""
from sqlalchemy import String, Boolean, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.base import TimestampMixin


class Warehouse(TimestampMixin, Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    capacity_tons: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    district: Mapped["District"] = relationship("District", back_populates="warehouses")

    def __repr__(self) -> str:
        return f"<Warehouse {self.name} (district={self.district_id})>"
