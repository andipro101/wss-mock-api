from __future__ import annotations

from sqlalchemy import JSON, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    admin_center: Mapped[str] = mapped_column(String, nullable=False)
    time_zone: Mapped[str | None] = mapped_column(String, nullable=True)
    menu_name: Mapped[str | None] = mapped_column(String, nullable=True)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    administrator: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    web_user: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    keep_tx_trader: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    locked_login: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_users: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_services: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_system: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_processes: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_components: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_entitlements: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    platform_profile: Mapped[str | None] = mapped_column(String, nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    database_login: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    database_login_original: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    locked_db_login: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    transitive: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sdm_state: Mapped[str] = mapped_column(String, nullable=False, default="FINAL")


class UserRoleAssignmentEntity(Base):
    __tablename__ = "user_role_assignments"

    user_id: Mapped[str] = mapped_column(String, primary_key=True)
    role_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_role_action: Mapped[str | None] = mapped_column(String, nullable=True)