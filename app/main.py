from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from app.db import init_db
from app.schemas import SingleResponsePojo, UserPojo, UserRoleAssignmentPojo
from app.seed import reset_database, seed_database_if_empty
from app.services import (
    create_users,
    get_user,
    get_user_role_assignments as fetch_user_role_assignments,
    list_role_assignments,
    list_users,
    override_role_assignments,
    purge_user,
    revoke_user,
    update_users,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_database_if_empty()
    yield


app = FastAPI(
    title="WSS Mock API",
    version="0.1.0",
    description=(
        "A local mock implementation of the Security Center REST API. "
        "Used for ISIM adapter development and TDI assembly line testing.\n\n"
        "**Test data:** Call `POST /test/reset` to wipe and re-seed the database with default users."
    ),
    lifespan=lifespan,
)


API_PREFIX = "/securitycenter/restapi"


def error_response(status_code: int, payload: SingleResponsePojo | list[SingleResponsePojo]) -> JSONResponse:
    if isinstance(payload, list):
        content = [item.model_dump() for item in payload]
    else:
        content = payload.model_dump()
    return JSONResponse(status_code=status_code, content=content)


@app.get("/health", tags=["Health"], summary="Health check")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get(f"{API_PREFIX}/user/", tags=["Users"], summary="Get all users", response_model=list[UserPojo])
def get_all_users() -> list[UserPojo]:
    return list_users()


@app.post(f"{API_PREFIX}/user/", tags=["Users"], summary="Create multiple users", response_model=list[SingleResponsePojo])
def create_multiple_users(users: list[UserPojo]) -> list[SingleResponsePojo] | JSONResponse:
    responses, has_failure = create_users(users)
    if has_failure:
        return error_response(400, responses)
    return responses


@app.patch(f"{API_PREFIX}/user/", tags=["Users"], summary="Update multiple users", response_model=list[SingleResponsePojo])
def update_multiple_users(users: list[UserPojo]) -> list[SingleResponsePojo] | JSONResponse:
    responses, has_failure = update_users(users)
    if has_failure:
        return error_response(400, responses)
    return responses


@app.get(f"{API_PREFIX}/user/{{userid}}", tags=["Users"], summary="Get a single user by ID", response_model=UserPojo)
def get_single_user(userid: str = Path(description="The ID of the user to retrieve")) -> UserPojo | JSONResponse:
    result = get_user(userid)
    if isinstance(result, SingleResponsePojo):
        return error_response(400, result)
    return result


@app.delete(f"{API_PREFIX}/user/{{userid}}", tags=["Users"], summary="Revoke a user — locks the user but keeps them in the system", response_model=SingleResponsePojo)
def revoke_single_user(userid: str = Path(description="The ID of the user to revoke")) -> SingleResponsePojo | JSONResponse:
    result = revoke_user(userid)
    if result.result == "Failure":
        return error_response(400, result)
    return result


@app.delete(f"{API_PREFIX}/user/purge/{{userid}}", tags=["Users"], summary="Purge a user — permanently removes the user from the system", response_model=SingleResponsePojo)
def purge_single_user(userid: str = Path(description="The ID of the user to purge")) -> SingleResponsePojo | JSONResponse:
    result = purge_user(userid)
    if result.result == "Failure":
        return error_response(400, result)
    return result


@app.get(f"{API_PREFIX}/userroleassignment/", tags=["Role Assignments"], summary="Get all user role assignments", response_model=list[UserRoleAssignmentPojo])
def get_all_user_role_assignments() -> list[UserRoleAssignmentPojo]:
    return list_role_assignments()


@app.post(f"{API_PREFIX}/userroleassignment/", tags=["Role Assignments"], summary="Override multiple user role assignments", response_model=list[SingleResponsePojo])
def override_multiple_user_role_assignments(
    assignments: list[UserRoleAssignmentPojo],
) -> list[SingleResponsePojo] | JSONResponse:
    responses, has_failure = override_role_assignments(assignments)
    if has_failure:
        return error_response(400, responses)
    return responses


@app.get(
    f"{API_PREFIX}/userroleassignment/{{userid}}",
    tags=["Role Assignments"],
    summary="Get all role assignments for a single user",
    response_model=list[UserRoleAssignmentPojo],
)
def get_user_role_assignments(userid: str = Path(description="The ID of the user to retrieve role assignments for")) -> list[UserRoleAssignmentPojo] | JSONResponse:
    result = fetch_user_role_assignments(userid)
    if isinstance(result, SingleResponsePojo):
        return error_response(400, result)
    return result


@app.post("/test/reset", tags=["Test Helpers"], summary="Reset test data — wipes the database and re-seeds default users")
def reset_test_data() -> dict[str, str]:
    reset_database()
    return {"status": "reset"}