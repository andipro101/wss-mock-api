from __future__ import annotations

from sqlalchemy import select

from app.db import SessionLocal
from app.models import UserEntity, UserRoleAssignmentEntity
from app.schemas import SingleResponsePojo, UserPojo, UserRoleAssignmentPojo


def list_users() -> list[UserPojo]:
    with SessionLocal() as session:
        entities = session.scalars(select(UserEntity).order_by(UserEntity.id)).all()
        return [user_from_entity(entity) for entity in entities]


def create_users(users: list[UserPojo]) -> tuple[list[SingleResponsePojo], bool]:
    responses: list[SingleResponsePojo] = []
    has_failure = False

    with SessionLocal() as session:
        for user in users:
            if session.get(UserEntity, user.id) is not None:
                has_failure = True
                responses.append(user_exists_error(user.id))
                continue

            session.add(user_to_entity(user, sdm_state="FINAL"))
            responses.append(success_response("User", user.id))

        session.commit()

    return responses, has_failure


def update_users(users: list[UserPojo]) -> tuple[list[SingleResponsePojo], bool]:
    responses: list[SingleResponsePojo] = []
    has_failure = False

    with SessionLocal() as session:
        for user in users:
            entity = session.get(UserEntity, user.id)
            if entity is None:
                has_failure = True
                responses.append(user_not_found_error(user.id))
                continue
            if entity.sdm_state != "FINAL":
                has_failure = True
                responses.append(not_final_error(user.id))
                continue

            apply_user_to_entity(entity, user)
            responses.append(success_response("User", user.id))

        session.commit()

    return responses, has_failure


def get_user(user_id: str) -> UserPojo | SingleResponsePojo:
    with SessionLocal() as session:
        entity = session.get(UserEntity, user_id)
        if entity is None:
            return user_not_found_error(user_id)
        return user_from_entity(entity)


def revoke_user(user_id: str) -> SingleResponsePojo:
    with SessionLocal() as session:
        entity = session.get(UserEntity, user_id)
        if entity is None:
            return user_not_found_error(user_id)
        if entity.sdm_state != "FINAL":
            return not_final_error(user_id)

        entity.locked_login = True
        session.commit()
        return success_response("User", user_id)


def purge_user(user_id: str) -> SingleResponsePojo:
    with SessionLocal() as session:
        entity = session.get(UserEntity, user_id)
        if entity is None:
            return user_not_found_error(user_id)
        if entity.sdm_state != "FINAL":
            return not_final_error(user_id)

        assignment = session.get(UserRoleAssignmentEntity, user_id)
        if assignment is not None:
            session.delete(assignment)
        session.delete(entity)
        session.commit()
        return success_response("User", user_id)


def list_role_assignments() -> list[UserRoleAssignmentPojo]:
    with SessionLocal() as session:
        entities = session.scalars(
            select(UserRoleAssignmentEntity).order_by(UserRoleAssignmentEntity.user_id)
        ).all()
        return [assignment_from_entity(entity) for entity in entities]


def override_role_assignments(
    assignments: list[UserRoleAssignmentPojo],
) -> tuple[list[SingleResponsePojo], bool]:
    responses: list[SingleResponsePojo] = []
    has_failure = False

    with SessionLocal() as session:
        for assignment in assignments:
            user = session.get(UserEntity, assignment.userId)
            if user is None:
                has_failure = True
                responses.append(user_not_found_error(assignment.userId))
                continue
            if user.sdm_state != "FINAL":
                has_failure = True
                responses.append(not_final_error(assignment.userId))
                continue

            entity = session.get(UserRoleAssignmentEntity, assignment.userId)
            if entity is None:
                entity = UserRoleAssignmentEntity(user_id=assignment.userId)
                session.add(entity)

            entity.role_ids = assignment.roleIDs
            entity.missing_role_action = assignment.missingRoleAction
            responses.append(success_response("UserRoleAssignment", assignment.userId))

        session.commit()

    return responses, has_failure


def get_user_role_assignments(user_id: str) -> list[UserRoleAssignmentPojo] | SingleResponsePojo:
    with SessionLocal() as session:
        user = session.get(UserEntity, user_id)
        if user is None:
            return user_not_found_error(user_id)

        entity = session.get(UserRoleAssignmentEntity, user_id)
        if entity is None:
            return []
        return [assignment_from_entity(entity)]


def success_response(entity_type: str, entity_id: str) -> SingleResponsePojo:
    return SingleResponsePojo(entityType=entity_type, entityId=entity_id, result="Success")


def user_exists_error(user_id: str) -> SingleResponsePojo:
    return SingleResponsePojo(
        entityType="User",
        entityId=user_id,
        result="Failure",
        errorMessage="A user with this ID already exists",
    )


def user_not_found_error(user_id: str) -> SingleResponsePojo:
    return SingleResponsePojo(
        entityType="User",
        entityId=user_id,
        result="Failure",
        errorMessage=f"User '{user_id}' does not exist",
    )


def not_final_error(user_id: str) -> SingleResponsePojo:
    return SingleResponsePojo(
        entityType="User",
        entityId=user_id,
        result="Failure",
        errorMessage=(
            "Entity is not in SDM FINAL state. Finalize it manually before calling the REST API."
        ),
    )


def user_from_entity(entity: UserEntity) -> UserPojo:
    return UserPojo(
        id=entity.id,
        name=entity.name,
        email=entity.email,
        adminCenter=entity.admin_center,
        timeZone=entity.time_zone,
        menuName=entity.menu_name,
        comment=entity.comment,
        administrator=entity.administrator,
        webUser=entity.web_user,
        keepTxTrader=entity.keep_tx_trader,
        lockedLogin=entity.locked_login,
        platformUsers=entity.platform_users,
        platformServices=entity.platform_services,
        platformSystem=entity.platform_system,
        platformProcesses=entity.platform_processes,
        platformComponents=entity.platform_components,
        platformEntitlements=entity.platform_entitlements,
        platformProfile=entity.platform_profile,
        version=entity.version,
        databaseLogin=entity.database_login,
        databaseLoginOriginal=entity.database_login_original,
        lockedDBLogin=entity.locked_db_login,
        transitive=entity.transitive,
    )


def assignment_from_entity(entity: UserRoleAssignmentEntity) -> UserRoleAssignmentPojo:
    return UserRoleAssignmentPojo(
        userId=entity.user_id,
        roleIDs=entity.role_ids,
        missingRoleAction=entity.missing_role_action,
    )


def user_to_entity(user: UserPojo, sdm_state: str) -> UserEntity:
    return UserEntity(
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
        sdm_state=sdm_state,
    )


def apply_user_to_entity(entity: UserEntity, user: UserPojo) -> None:
    entity.name = user.name
    entity.email = user.email
    entity.admin_center = user.adminCenter
    entity.time_zone = user.timeZone
    entity.menu_name = user.menuName
    entity.comment = user.comment
    entity.administrator = user.administrator
    entity.web_user = user.webUser
    entity.keep_tx_trader = user.keepTxTrader
    entity.locked_login = user.lockedLogin
    entity.platform_users = user.platformUsers
    entity.platform_services = user.platformServices
    entity.platform_system = user.platformSystem
    entity.platform_processes = user.platformProcesses
    entity.platform_components = user.platformComponents
    entity.platform_entitlements = user.platformEntitlements
    entity.platform_profile = user.platformProfile
    entity.version = user.version
    entity.database_login = user.databaseLogin
    entity.database_login_original = user.databaseLoginOriginal
    entity.locked_db_login = user.lockedDBLogin
    entity.transitive = user.transitive