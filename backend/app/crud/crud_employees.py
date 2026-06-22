import uuid
from typing import Any

from sqlmodel import Session, col, func, select

from app.models.employee import EmployeeCreate, EmployeeUpdate
from app.models.employee import Employee


def create_employee(
    *, session: Session, employee_in: EmployeeCreate
) -> Employee:
    db_employee = Employee.model_validate(employee_in)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def get_employee_by_id(
    *, session: Session, employee_id: uuid.UUID
) -> Employee | None:
    return session.get(Employee, employee_id)


def get_employee_by_email(
    *, session: Session, email: str
) -> Employee | None:
    statement = select(Employee).where(Employee.email == email)
    return session.exec(statement).first()


def get_employees(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[list[Employee], int]:
    count_statement = select(func.count()).select_from(Employee)
    count = session.exec(count_statement).one()

    statement = (
        select(Employee)
        .order_by(col(Employee.created_at).desc(), col(Employee.id).desc())
        .offset(skip)
        .limit(limit)
    )
    employees = session.exec(statement).all()
    return list(employees), count


def update_employee(
    *, session: Session, db_employee: Employee, employee_in: EmployeeUpdate
) -> Any:
    employee_data = employee_in.model_dump(exclude_unset=True)
    db_employee.sqlmodel_update(employee_data)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def delete_employee(*, session: Session, db_employee: Employee) -> None:
    session.delete(db_employee)
    session.commit()
