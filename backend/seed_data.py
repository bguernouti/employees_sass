import logging
import random
from datetime import datetime, timedelta

from sqlmodel import Session, func, select

from app.core.db import engine
from app.models.employee import Employee

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

first_names = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes",
]

positions = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer",
    "Product Manager", "Senior Product Manager", "Data Scientist",
    "DevOps Engineer", "SRE", "UX Designer", "QA Engineer",
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Engineering Manager", "Technical Writer", "Security Engineer",
    "Mobile Developer", "Data Engineer", "ML Engineer", "Solutions Architect",
    "Business Analyst", "Project Manager", "Scrum Master", "VP of Engineering",
    "CTO", "CEO", "COO", "CFO", "HR Manager", "Recruiter",
    "Marketing Manager", "Sales Representative", "Account Executive",
    "Customer Success Manager", "Support Engineer", "IT Administrator",
]

departments = [
    "Engineering", "Product", "Design", "Data", "DevOps",
    "Security", "Marketing", "Sales", "Human Resources",
    "Finance", "Operations", "Customer Success", "IT",
    "Research", "Legal", "Administration",
]


def seed() -> None:
    with Session(engine) as session:
        existing_count = session.exec(
            select(func.count()).select_from(Employee)
        ).one()
        if existing_count > 0:
            logger.info(f"{existing_count} employees already exist, skipping seed")
            return

        employees = []
        used_emails = set()
        for i in range(500):
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
            while email in used_emails:
                email = f"{first.lower()}.{last.lower()}{random.randint(0,99999)}@example.com"
            used_emails.add(email)

            position = random.choice(positions)
            department = random.choice(departments)
            days_ago = random.randint(0, 365 * 5)
            hire_date = datetime.now() - timedelta(days=days_ago)
            salary = round(random.uniform(40000, 200000), 2)
            phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"

            emp = Employee(
                full_name=full_name,
                email=email,
                phone=phone,
                position=position,
                department=department,
                hire_date=hire_date,
                salary=salary,
                is_active=random.random() > 0.1,
            )
            employees.append(emp)

        session.add_all(employees)
        session.commit()
        logger.info(f"Inserted {len(employees)} employees")


def main() -> None:
    logger.info("Seeding database")
    seed()
    logger.info("Seeding complete")


if __name__ == "__main__":
    main()
