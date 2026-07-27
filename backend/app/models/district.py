"""
District and Taluk geographic hierarchy models.
"""
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.base import TimestampMixin


class District(TimestampMixin, Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, default="Tamil Nadu")
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    taluks: Mapped[list["Taluk"]] = relationship(
        "Taluk", back_populates="district", cascade="all, delete-orphan", lazy="selectin"
    )
    shops: Mapped[list["FairPriceShop"]] = relationship(
        "FairPriceShop", back_populates="district"
    )
    warehouses: Mapped[list["Warehouse"]] = relationship(
        "Warehouse", back_populates="district"
    )
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="district", foreign_keys="User.district_id"
    )

    def __repr__(self) -> str:
        return f"<District {self.name} ({self.code})>"


class Taluk(TimestampMixin, Base):
    __tablename__ = "taluks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    district: Mapped["District"] = relationship("District", back_populates="taluks")
    shops: Mapped[list["FairPriceShop"]] = relationship(
        "FairPriceShop", back_populates="taluk"
    )
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="taluk", foreign_keys="User.taluk_id"
    )

    def __repr__(self) -> str:
        return f"<Taluk {self.name} ({self.code})>"
