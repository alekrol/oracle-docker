import csv
import random
import pandas as pd
from pathlib import Path

from datetime import date, datetime
from .models import (
    SwimmingClass,
    SwimmingPool,
    SwimmingSchool,
    Instructor,
    CoursePayment,
    Customer,
    Multisport,
)

from .generation_helpers import (
    MAILS,
    DOMAINS,
    PHONE_PREFIXES,
    random_date,
    serialize_str,
    generate_birth_date,
    generate_mail,
    generate_number,
    generate_name_and_surname,
)

EXAMPLE_DATA_PATH = Path("example-data/")
DATA_FOR_DB_IMPORT_PATH = Path("data-for-db-import/")

random.seed(42)

def generate_swimming_school_data() -> int:
    header = "id name city capacity description built_date last_renovation_date".split()

    def swimming_school_to_row(s: SwimmingSchool) -> list[SwimmingSchool]:
        return [
            s.id,
            s.name,
            s.city,
            s.capacity,
            s.description,
            s.built_date,
            s.last_renovation_date,
        ]

    with open(EXAMPLE_DATA_PATH + "cities.csv", "r") as cities_file, open(
        EXAMPLE_DATA_PATH + "swimming-schools-descriptions.csv", "r"
    ) as descriptions_file, open(
        EXAMPLE_DATA_PATH + "swimming-school-names.csv", "r"
    ) as names_file, open(
        DATA_FOR_DB_IMPORT_PATH + "swimming-schools.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as schools_file:

        writer = csv.writer(schools_file)
        writer.writerow(header)

        saved_schools = 0

        names = [row["name"] for row in csv.DictReader(names_file)]
        descriptions = [row["description"] for row in csv.DictReader(descriptions_file)]
        cities = [row["city"] for row in csv.DictReader(cities_file)]

        for i, (name, city, description) in enumerate(
            zip(names, cities, descriptions), start=1
        ):
            built_date = random_date(date(1990, 1, 1), date(2024, 1, 1))
            last_renovation_date = random_date(built_date, date(2025, 1, 1))

            swimming_school = SwimmingSchool(
                id=i,
                name=name,
                city=city,
                capacity=random.randint(50, 1000),
                description=description,
                built_date=built_date,
                last_renovation_date=last_renovation_date,
            )

            writer.writerow(swimming_school_to_row(swimming_school))
            saved_schools += 1

    return saved_schools

def generate_customer_data(n=100000) -> None:
    def customer_to_row(c: Customer):
        return [
            c.id,
            c.swimming_school_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.is_disabled,
            c.birth_date.isoformat(),  # lepiej do CSV
            c.is_active,
        ]

    with open(
        DATA_FOR_DB_IMPORT_PATH + "swimming-schools.csv", "r"
    ) as swimming_schools_file, open(
        DATA_FOR_DB_IMPORT_PATH + "customers.csv", "w", encoding="utf-8", newline=""
    ) as customers_file:

        swimming_schools_ids = [r["id"] for r in csv.DictReader(swimming_schools_file)]

        customers_saved = 0

        writer = csv.writer(customers_file)
        writer.writerow(
            "id swimming_school_id first_name last_name email phone is_disabled birth_date is_active".split()
        )

        for i in range(1, n + 1):
            first_name, last_name = generate_name_and_surname()

            # correct polish last-name in case of a woman
            if first_name[-1] == "a" and last_name[-1] != "a":
                last_name = last_name[:-1] + "a"

            customer = Customer(
                id=i,
                swimming_school_id=random.choice(swimming_schools_ids),
                first_name=first_name,
                last_name=last_name,
                email=generate_mail(first_name, last_name),
                phone=generate_number(),
                birth_date=generate_birth_date(),
                is_disabled=random.random() < 0.01,  # 1/100 is disabled
                is_active=random.random() < 0.85,
            )

            writer.writerow(customer_to_row(customer))
            customers_saved += 1

    print(f'customer data saved: {customers_saved}') 

def generate_instructor_data(n=1000) -> None:
    swimming_schools_path = DATA_FOR_DB_IMPORT_PATH / "swimming-schools.csv"
    instructor_path = DATA_FOR_DB_IMPORT_PATH / "instructors.csv"

    written_instructors = 0

    if not swimming_schools_path.exists():
        raise Exception("swimming-schools.csv file not found!")

    df = pd.read_csv(swimming_schools_path, usecols=["id", "built_date"])

    swimming_school_infos = list(zip(df["id"], df["built_date"]))

    with open(instructor_path, "w") as f:
        writer = csv.writer(f)

        csv_header = "id first_name last_name swimming_school_id phone_num empoyment_date salary".split()
        writer.writerow(csv_header)

        for i in range(1, n + 1):
            name, last_name = generate_name_and_surname()
            swimming_school_id, swimming_school_built_date = random.choice(
                swimming_school_infos
            )
            swimming_school_built_date = datetime.strptime(swimming_school_built_date, '%Y-%m-%d').date()

            instructor = Instructor(
                id=i,
                first_name=name,
                last_name=last_name,
                swimming_school_id=swimming_school_id,
                employment_date=random_date(swimming_school_built_date, date(2026, 1, 1)),
                salary=random.randint(50, 100) * 100,
                phone_num=generate_number(),
            )

            writer.writerow(instructor.field_values_to_list())
            written_instructors += 1

    print(f"instructor data saved: {written_instructors}")


if __name__ == "__main__":
    generate_instructor_data()
