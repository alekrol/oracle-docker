import csv
import random
import pandas as pd
from pathlib import Path
from dataclasses import fields
from datetime import date, datetime, timedelta

from .models import (
    SwimmingClass,
    SwimmingPool,
    SwimmingSchool,
    Instructor,
    CoursePayment,
    Customer,
    Multisport,
    Course,
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

DATA_DICTIONARY_PATH = Path("data-dictionary/")
DATA_FOR_DB_IMPORT_PATH = Path("data-for-db-import/")

random.seed(42)


def generate_swimming_school_data() -> None:
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

    print(f"schools data saved: {saved_schools}")


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

    print(f"customer data saved: {customers_saved}")


def generate_instructor_data(n=1000) -> None:
    swimming_schools_path = DATA_FOR_DB_IMPORT_PATH / "swimming-schools.csv"
    instructor_path = DATA_FOR_DB_IMPORT_PATH / "instructors.csv"

    written_instructors = 0

    if not swimming_schools_path.exists():
        raise Exception("swimming-schools.csv file not found!")

    df = pd.read_csv(swimming_schools_path, usecols=["id", "built_date"])

    swimming_school_infos = list(zip(df["id"], df["built_date"]))

    with open(instructor_path, "w", newline="") as f:
        writer = csv.writer(f)

        csv_header = "id first_name last_name swimming_school_id phone_num empoyment_date salary".split()
        writer.writerow(csv_header)

        for i in range(1, n + 1):
            name, last_name = generate_name_and_surname()
            swimming_school_id, swimming_school_built_date = random.choice(
                swimming_school_infos
            )
            swimming_school_built_date = datetime.strptime(
                swimming_school_built_date, "%Y-%m-%d"
            ).date()

            instructor = Instructor(
                id=i,
                first_name=name,
                last_name=last_name,
                swimming_school_id=swimming_school_id,
                employment_date=random_date(
                    swimming_school_built_date, date(2026, 1, 1)
                ),
                salary=random.randint(50, 100) * 100,
                phone_num=generate_number(),
            )

            writer.writerow(instructor.field_values_to_list())
            written_instructors += 1

    print(f"instructor data saved: {written_instructors}")


def generate_multisport_data(ms_percent: int = 80) -> None:
    """
    Generate multisport data for *ms_percent* of customers
    """

    customers_path = DATA_FOR_DB_IMPORT_PATH / "customers.csv"
    multisports_path = DATA_FOR_DB_IMPORT_PATH / "multisports.csv"

    if not customers_path.exists():
        raise Exception("customers.csv file not found!")

    customer_ids = pd.read_csv(customers_path, usecols=["id"])["id"].to_list()
    multisport_count = int(ms_percent * len(customer_ids) / 100)
    customer_with_multisport_ids = iter(
        random.sample(customer_ids, k=multisport_count)
    )  # assume that 8/10 customers have a multisport card
    multisports_saved = 0

    with open(multisports_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f.name for f in fields(Multisport)]

        writer.writerow(header)

        for i in range(1, multisport_count + 1):
            multisport = Multisport(
                id=i,
                customer_id=next(customer_with_multisport_ids),
                discount_percent=random.choice([20, 30, 40, 80, 100]),
                valid_until=random_date(date(2026, 1, 1), date(2029, 1, 1)),
                entries_left=random.choice([5, 10, 20, 30]),
            )

            writer.writerow(multisport.field_values_to_list())
            multisports_saved += 1

        print(f"customers saved: {multisports_saved}")


def generate_course_data() -> None:
    path_swimming_schools = DATA_FOR_DB_IMPORT_PATH / "swimming-schools.csv"
    path_course_descriptions = DATA_DICTIONARY_PATH / "course-descriptions.csv"
    path_instructors = DATA_FOR_DB_IMPORT_PATH / "instructors.csv"
    path_courses = DATA_FOR_DB_IMPORT_PATH / "courses.csv"

    for path in [path_swimming_schools, path_course_descriptions, path_instructors]:
        if not path.exists():
            raise Exception(f"{path.name} file not found!")

    df_instructors = pd.read_csv(path_instructors, usecols=["id", "swimming_school_id"])
    df_courses = pd.read_csv(path_course_descriptions, usecols=["id", "description"])
    df_swimming_schools = pd.read_csv(
        path_swimming_schools, usecols=["id", "built_date"]
    )

    instructors = list(zip(df_instructors["id"], df_instructors["swimming_school_id"]))
    courses = list(zip(df_courses["id"], df_courses["description"]))
    swimming_schools = list(
        zip(df_swimming_schools["id"], df_swimming_schools["built_date"])
    )

    saved_courses = 0

    with open(path_courses, "w", newline="") as f:
        writer = csv.writer(f)
        header = [f.name for f in list(fields(Course))]

        writer.writerow(header)

        for id, description in courses:
            instructor_id, instructor_swimming_school_id = random.choice(instructors)
            swimming_school_id, swimming_school_built_date = random.choice(
                swimming_schools
            )
            swimming_school_built_date = datetime.strptime(
                swimming_school_built_date, "%Y-%m-%d"
            ).date()
            times_per_week = random.choice([1, 2, 3, 4])
            num_of_classes = times_per_week * random.choice([1, 2, 3, 4])
            date_start = random_date(swimming_school_built_date, date(2026, 1, 1))
            date_end = (
                date_start + timedelta(weeks=num_of_classes / times_per_week)
            ).strftime("%Y-%m-%d")

            course = Course(
                id=id,
                description=description,
                instructor_id=instructor_id,
                swimming_school_id=swimming_school_id,
                times_per_week=times_per_week,
                num_of_classes=num_of_classes,
                price=num_of_classes * 100,
                max_num_of_participants=random.choice([10, 15, 20]),
                is_multisport_accepted=random.random() > 0.05,
                date_start=date_start,
                date_end=date_end,
            )

            writer.writerow(course.field_values_to_list())
            saved_courses += 1

    print(f"saved courses: {saved_courses}")


if __name__ == "__main__":
    generate_course_data()
