"""
Models package — import all models so Base.metadata is fully populated for Alembic.
"""
from app.models.base import TimestampMixin
from app.models.role import Role, RoleName
from app.models.permission import Permission, RolePermission
from app.models.district import District, Taluk
from app.models.shop import FairPriceShop
from app.models.warehouse import Warehouse
from app.models.user import User

__all__ = [
    "TimestampMixin",
    "Role",
    "RoleName",
    "Permission",
    "RolePermission",
    "District",
    "Taluk",
    "FairPriceShop",
    "Warehouse",
    "User",
]
