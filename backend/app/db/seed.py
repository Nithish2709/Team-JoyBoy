"""
Seed script to populate initial roles, permissions, and a default superuser account.
"""
import asyncio
from sqlalchemy import select
from app.db.database import async_session_maker, import_models
from app.models.role import Role, RoleName
from app.models.user import User
from app.core.security import hash_password

import_models()


async def seed_data() -> None:
    print("Seeding initial database data...")
    async with async_session_maker() as session:
        # 1. Seed Roles if they don't exist
        for role_name in RoleName:
            result = await session.execute(
                select(Role).where(Role.name == role_name)
            )
            role = result.scalar_one_or_none()
            if not role:
                print(f"Creating role: {role_name.value}")
                session.add(Role(name=role_name, description=f"{role_name.value.replace('_', ' ').title()} role"))

        await session.commit()

        # Get super_admin role id
        result = await session.execute(
            select(Role.id).where(Role.name == RoleName.SUPER_ADMIN)
        )
        super_admin_role_id = result.scalar_one()

        # 2. Seed Default Super Admin User if doesn't exist
        admin_email = "admin@pds.gov.in"
        result = await session.execute(
            select(User).where(User.email == admin_email)
        )
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            print(f"Creating default super admin: {admin_email}")
            new_admin = User(
                email=admin_email,
                hashed_password=hash_password("Admin@1234"),
                full_name="System Super Administrator",
                role_id=super_admin_role_id,
                is_active=True,
            )
            session.add(new_admin)
            await session.commit()
            print("Default super admin created successfully!")
        else:
            print("Super admin user already exists.")

    print("Seeding process completed.")


if __name__ == "__main__":
    asyncio.run(seed_data())
