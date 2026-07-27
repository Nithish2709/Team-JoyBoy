"""
User model — platform accounts with RBAC role and geographic assignment.
"""
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.base import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id", ondelete="SET NULL"), nullable=True, index=True
    )
    taluk_id: Mapped[int | None] = mapped_column(
        ForeignKey("taluks.id", ondelete="SET NULL"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")
    district: Mapped["District | None"] = relationship(
        "District", back_populates="users", foreign_keys=[district_id], lazy="selectin"
    )
    taluk: Mapped["Taluk | None"] = relationship(
        "Taluk", back_populates="users", foreign_keys=[taluk_id], lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User {self.email} role={self.role_id}>"
