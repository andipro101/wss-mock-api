from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SingleResponsePojo(BaseModel):
    entityType: str
    entityId: str
    result: str
    errorMessage: str | None = None


class UserPojo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    email: str | None
    adminCenter: str
    timeZone: str | None = None
    menuName: str | None = None
    comment: str | None = None
    administrator: bool | None = None
    webUser: bool | None = None
    keepTxTrader: bool | None = None
    lockedLogin: bool | None = None
    platformUsers: bool | None = None
    platformServices: bool | None = None
    platformSystem: bool | None = None
    platformProcesses: bool | None = None
    platformComponents: bool | None = None
    platformEntitlements: bool | None = None
    platformProfile: str | None = None
    version: int | None = None
    databaseLogin: bool | None = None
    databaseLoginOriginal: bool | None = None
    lockedDBLogin: bool | None = None
    transitive: bool | None = None


class UserRoleAssignmentPojo(BaseModel):
    userId: str
    roleIDs: list[str] = Field(default_factory=list)
    missingRoleAction: Literal["Create", "Fail", "Ignore"] | None = "Ignore"


class SeedUser(BaseModel):
    user: UserPojo
    sdmState: Literal["FINAL", "DRAFT"] = "FINAL"