"""
FairPriceShop model — PDS retail distribution outlets.
"""
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.base import TimestampMixin


class FairPriceShop(TimestampMixin, Base):
    __tablename__ = "fair_price_shops"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shop_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    owner_name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    taluk_id: Mapped[int] = mapped_column(
        ForeignKey("taluks.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    district: Mapped["District"] = relationship("District", back_populates="shops")
    taluk: Mapped["Taluk"] = relationship("Taluk", back_populates="shops")

    def __repr__(self) -> str:
        return f"<FairPriceShop {self.shop_number} - {self.name}>"
