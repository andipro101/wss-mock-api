from __future__ import annotations

from sqlalchemy import delete, func, select

from app.db import SessionLocal
from app.models import UserEntity, UserRoleAssignmentEntity
from app.schemas import SeedUser, UserPojo, UserRoleAssignmentPojo


def default_users() -> list[SeedUser]:
    return [
        SeedUser(
            user=UserPojo(
                id="user1",
                name="Pierre",
                email="pierre@email.com",
                adminCenter="ROOT-ADMIN-CENTER",
                timeZone="UTC",
                menuName="SYSTEM-MENU",
                administrator=True,
                webUser=True,
                platformUsers=True,
                platformProfile="Administrator",
                version=0,
            ),
            sdmState="FINAL",
        ),
        SeedUser(
            user=UserPojo(
                id="svsupport9",
                name="Galin",
                email=None,
                adminCenter="ROOT-ADMIN-CENTER",
                timeZone="EET",
                menuName="BNB-MENU",
                comment=None,
                administrator=False,
                webUser=False,
                keepTxTrader=False,
                lockedLogin=False,
                platformUsers=False,
                platformServices=False,
                platformSystem=False,
                platformProcesses=False,
                platformComponents=False,
                platformEntitlements=False,
                platformProfile="Viewer",
                version=0,
                databaseLogin=False,
                databaseLoginOriginal=False,
                lockedDBLogin=False,
                transitive=False,
            ),
            sdmState="FINAL",
        ),
        SeedUser(
            user=UserPojo(
                id="draft-user",
                name="Draft User",
                email="draft.user@email.com",
                adminCenter="ROOT-ADMIN-CENTER",
                comment="Used to simulate non-FINAL entity failures",
                lockedLogin=False,
                version=0,
            ),
            sdmState="DRAFT",
        ),
    ]


def default_role_assignments() -> list[UserRoleAssignmentPojo]:
    return [
        UserRoleAssignmentPojo(
            userId="user1",
            roleIDs=["ACCOUNTANT", "ADMINISTRATOR"],
            missingRoleAction="Ignore",
        ),
        UserRoleAssignmentPojo(
            userId="svsupport9",
            roleIDs=["VIEWER"],
            missingRoleAction="Ignore",
        ),
        UserRoleAssignmentPojo(
            userId="draft-user",
            roleIDs=["BACK-OFFICE"],
            missingRoleAction="Ignore",
        ),
    ]


def seed_database_if_empty() -> None:
    with SessionLocal() as session:
        user_count = session.scalar(select(func.count()).select_from(UserEntity))
        if user_count:
            return
    reset_database()


def reset_database() -> None:
    with SessionLocal() as session:
        session.execute(delete(UserRoleAssignmentEntity))
        session.execute(delete(UserEntity))

        for seed_user in default_users():
            user = seed_user.user
            session.add(
                UserEntity(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    admin_center=user.adminCenter,
                    time_zone=user.timeZone,
                    menu_name=user.menuName,
                    comment=user.comment,
                    administrator=user.administrator,
                    web_user=user.webUser,
                    keep_tx_trader=user.keepTxTrader,
                    locked_login=user.lockedLogin,
                    platform_users=user.platformUsers,
                    platform_services=user.platformServices,
                    platform_system=user.platformSystem,
                    platform_processes=user.platformProcesses,
                    platform_components=user.platformComponents,
                    platform_entitlements=user.platformEntitlements,
                    platform_profile=user.platformProfile,
                    version=user.version,
                    database_login=user.databaseLogin,
                    database_login_original=user.databaseLoginOriginal,
                    locked_db_login=user.lockedDBLogin,
                    transitive=user.transitive,
                    sdm_state=seed_user.sdmState,
                )
            )

        for assignment in default_role_assignments():
            session.add(
                UserRoleAssignmentEntity(
                    user_id=assignment.userId,
                    role_ids=assignment.roleIDs,
                    missing_role_action=assignment.missingRoleAction,
                )
            )

        session.commit()