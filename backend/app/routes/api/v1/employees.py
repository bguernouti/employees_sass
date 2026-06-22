import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    EmployeeCreate,
    EmployeePublic,
    EmployeesPublic,
    EmployeeUpdate,
    Message,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=EmployeesPublic)
def read_employees(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    employees, count = crud.get_employees(
        session=session, skip=skip, limit=limit
    )

    employees_public = [EmployeePublic.model_validate(emp) for emp in employees]
    return EmployeesPublic(data=employees_public, count=count)


@router.get("/{id}", response_model=EmployeePublic)
def read_employee(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> Any:
    employee = crud.get_employee_by_id(session=session, employee_id=id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("/", response_model=EmployeePublic)
def create_employee(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    employee_in: EmployeeCreate,
) -> Any:
    existing = crud.get_employee_by_email(session=session, email=employee_in.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="An employee with this email already exists in the system.",
        )
    employee = crud.create_employee(
        session=session, employee_in=employee_in
    )
    return employee


@router.put("/{id}", response_model=EmployeePublic)
def update_employee(
    *,
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
    employee_in: EmployeeUpdate,
) -> Any:
    employee = crud.get_employee_by_id(session=session, employee_id=id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = crud.update_employee(
        session=session, db_employee=employee, employee_in=employee_in
    )
    return employee


@router.delete("/{id}")
def delete_employee(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> Message:
    employee = crud.get_employee_by_id(session=session, employee_id=id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(session=session, db_employee=employee)
    return Message(message="Employee deleted successfully")
