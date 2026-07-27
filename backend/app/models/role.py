"""
Role model — defines system roles for RBAC.
"""
import enum
from sqlalchemy import String, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.base import TimestampMixin


class RoleName(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    STATE_OFFICER = "state_officer"
    DISTRICT_OFFICER = "district_officer"
    TALUK_OFFICER = "taluk_officer"
    INSPECTOR = "inspector"


class Role(TimestampMixin, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[RoleName] = mapped_column(
        SAEnum(RoleName, name="role_name_enum"),
        unique=True,
        nullable=False,
        index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    users: Mapped[list["User"]] = relationship("User", back_populates="role", lazy="selectin")
    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission", back_populates="role", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Role {self.name}>"
