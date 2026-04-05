import csv
import random
import pandas as pd
import numpy as np
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

# AI-generated dictionary data to base on
path_course_descriptions = DATA_DICTIONARY_PATH / "course-descriptions.csv"
path_swimming_school_descriptions = (
    DATA_DICTIONARY_PATH / "swimming-schools-descriptions.csv"
)
path_swimming_school_names = DATA_DICTIONARY_PATH / "swimming-school-names.csv"
path_cities = DATA_DICTIONARY_PATH / "cities.csv"

# output files (also used as input for related tables)
path_swimming_schools = DATA_FOR_DB_IMPORT_PATH / "swimming-schools.csv"
path_instructors = DATA_FOR_DB_IMPORT_PATH / "instructors.csv"
path_courses = DATA_FOR_DB_IMPORT_PATH / "courses.csv"
path_customers = DATA_FOR_DB_IMPORT_PATH / "customers.csv"
path_multisport = DATA_FOR_DB_IMPORT_PATH / "multisports.csv"
path_instructors = DATA_FOR_DB_IMPORT_PATH / "instructors.csv"
path_course_payments = DATA_FOR_DB_IMPORT_PATH / "course-payments.csv"
path_swimming_pools = DATA_FOR_DB_IMPORT_PATH / "swimming-pools.csv"

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

    with open(path_cities, "r") as cities_file, open(
        path_swimming_school_descriptions, "r"
    ) as descriptions_file, open(path_swimming_school_names, "r") as names_file, open(
        path_swimming_schools,
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

    with open(path_swimming_schools, "r") as swimming_schools_file, open(
        path_customers, "w", encoding="utf-8", newline=""
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
    written_instructors = 0

    if not path_swimming_schools.exists():
        raise Exception("swimming-schools.csv file not found!")

    df = pd.read_csv(path_swimming_schools, usecols=["id", "built_date"])

    swimming_school_infos = list(zip(df["id"], df["built_date"]))

    with open(path_instructors, "w", newline="") as f:
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

    if not path_customers.exists():
        raise Exception("customers.csv file not found!")

    customer_ids = pd.read_csv(path_customers, usecols=["id"])["id"].to_list()
    multisport_count = int(ms_percent * len(customer_ids) / 100)
    customer_with_multisport_ids = iter(
        random.sample(customer_ids, k=multisport_count)
    )  # assume that 8/10 customers have a multisport card
    multisports_saved = 0

    with open(path_multisport, "w", newline="") as f:
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


def generate_course_payment_data() -> None:
    df_courses = pd.read_csv(
        path_courses,
        usecols=[
            "id",
            "price",
            "is_multisport_accepted",
            "max_num_of_participants",
        ],
    )

    df_multisports = pd.read_csv(
        path_multisport,
        usecols=["customer_id", "discount_percent", "valid_until"],
    )

    df_customers = pd.read_csv(path_customers, usecols=["id"])

    participants_per_course = (
        df_courses["max_num_of_participants"]
        - np.random.randint(0, 4, size=len(df_courses))
    ).clip(lower=0)

    df_course_payments = pd.DataFrame()

    df_course_payments["course_id"] = (
        df_courses["id"]
        .loc[df_courses.index.repeat(participants_per_course)]
        .reset_index(drop=True)
    )

    df_course_payments["customer_id"] = np.random.choice(
        df_customers["id"],
        size=len(df_course_payments),
        replace=True,
    )

    df_course_payments["status"] = random.choices(
        [s.name for s in CoursePayment.Status],
        weights=CoursePayment.STATUS_WEIGHTS,
        k=len(df_course_payments),
    )

    df_course_payments["id"] = np.arange(1, len(df_course_payments) + 1)

    start = np.datetime64("2023-01-01")
    end = np.datetime64("2023-12-31")
    df_course_payments["created_at"] = start + (end - start) * np.random.rand(
        len(df_course_payments)
    )

    df_course_payments["description"] = ""

    df_course_payments = (
        df_course_payments.merge(
            df_courses[["id", "price", "is_multisport_accepted"]],
            left_on="course_id",
            right_on="id",
            how="left",
        )
        .drop(columns="id_y", errors="ignore")
        .rename(columns={"id_x": "id"})
        .merge(
            df_multisports[["customer_id", "discount_percent", "valid_until"]],
            on="customer_id",
            how="left",
        )
    )

    today = pd.Timestamp.today().normalize()
    df_course_payments["valid_until"] = pd.to_datetime(
        df_course_payments["valid_until"], errors="coerce"
    )

    has_valid_multisport = (
        df_course_payments["discount_percent"].notna()
        & (df_course_payments["valid_until"] >= today)
    )

    can_use_multisport = (
        has_valid_multisport & df_course_payments["is_multisport_accepted"]
    )

    df_course_payments["amount_paid"] = np.where(
        can_use_multisport,
        df_course_payments["price"]
        * (1 - df_course_payments["discount_percent"] / 100),
        df_course_payments["price"],
    ).round(2)

    df_course_payments = df_course_payments[
        [
            "id",
            "course_id",
            "customer_id",
            "status",
            "created_at",
            "description",
            "amount_paid",
        ]
    ]

    df_course_payments.to_csv(path_course_payments, index=False, encoding="utf-8")


def generate_swimming_pool_data(n=10)->None:
    """
    generate *n* pool instances per swimming school
    """

    swimming_school_ids = pd.read_csv(path_swimming_schools, usecols=["id"])["id"]

    with open(path_swimming_pools, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = [f.name for f in fields(SwimmingPool)]

        writer.writerow(header)
        saved_rows = 0

        for i, school_id in enumerate(swimming_school_ids, start=1):
            for j in range(n):
                num_of_lanes = random.choice([4, 6, 8, 10, 12, 15])
                max_capacity = num_of_lanes * 6

                swimming_pool = SwimmingPool(
                    id=i+j,
                    swimming_school_id=school_id,
                    max_depth=random.choice([160 + 10 * i for i in range(10)]),
                    min_depth=random.choice([100, 120, 140, 150]),
                    is_for_disabled=random.random() < 0.80,
                    num_of_lanes=num_of_lanes,
                    max_capacity=max_capacity,
                    is_olympic=random.choice([True, False]),
                    length=random.choice([25, 40, 50]),
                )

                writer.writerow(swimming_pool.field_values_to_list())
                saved_rows += 1

    print(f'written {saved_rows} swimming pool data rows') 


if __name__ == "__main__":
    generate_course_payment_data()
