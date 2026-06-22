from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel

from app.models.common import get_datetime_utc


class EmployeeBase(SQLModel):
    full_name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=255)
    department: str | None = Field(default=None, max_length=255)
    hire_date: datetime | None = None
    salary: float | None = None
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=255)
    department: str | None = Field(default=None, max_length=255)
    hire_date: datetime | None = None
    salary: float | None = None
    is_active: bool | None = None


class EmployeePublic(EmployeeBase):
    id: uuid.UUID
    created_at: datetime | None = None


class EmployeesPublic(SQLModel):
    data: list[EmployeePublic]
    count: int


class Employee(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str = Field(max_length=255)
    email: str = Field(unique=True, index=True, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=255)
    department: str | None = Field(default=None, max_length=255)
    hire_date: datetime | None = None
    salary: float | None = None
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
