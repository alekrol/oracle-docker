import csv
import random

from datetime import date, timedelta
from .models import (
    SwimmingClass,
    SwimmingPool,
    SwimmingSchool,
    Instructor,
    CoursePayment,
    Customer,
    Multisport,
)

EXAMPLE_DATA_PATH = "example-data/"
DATA_FOR_DV_IMPORT_PATH = "data-for-db-import/"

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

    def random_date(start: date, end: date) -> date:
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    with open(EXAMPLE_DATA_PATH + "cities.csv", "r") as cities_file, open(
        EXAMPLE_DATA_PATH + "swimming-schools-descriptions.csv", "r"
    ) as descriptions_file, open(
        EXAMPLE_DATA_PATH + "swimming-school-names.csv", "r"
    ) as names_file, open(
        DATA_FOR_DV_IMPORT_PATH + "swimming-schools.csv",
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


def generate_customer_data(n=100000) -> int:
    def generate_number() -> str:
        return random.choice(PHONE_PREFIXES) + "".join(
            [str(random.randint(0, 9)) for _ in range(9)]
        )

    def generate_mail(first_name: str, last_name: str) -> str:
        return serialize_str(
            first_name[:3].lower()
            + "."
            + last_name[:3].lower()
            + str(random.randint(0, 1000))
            + "@"
            + random.choice(MAILS)
            + "."
            + random.choice(DOMAINS)
        )

    def generate_birth_date():
        start = date(1950, 1, 1)
        end = date(2020, 1, 1)

        return start + timedelta(days=random.randint(0, (end - start).days))

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

    def serialize_str(s: str):
        PL_TO_ASCII = {
            "ą": "a",
            "ć": "c",
            "ę": "e",
            "ł": "l",
            "ń": "n",
            "ó": "o",
            "ś": "s",
            "ź": "z",
            "ż": "z",
        }

        return ''.join(PL_TO_ASCII.get(c, c) for c in s)

    MAILS = "gmail o2 yahoo bing wp outlook company".split()
    DOMAINS = "pl en com us gov eu de fr io".split()
    PHONE_PREFIXES = "+48 +212 +12 +10 +42 +13 +65 +11".split()

    with open(EXAMPLE_DATA_PATH + "first-names.csv", "r") as first_names_file, open(
        EXAMPLE_DATA_PATH + "last-names.csv", "r"
    ) as last_names_file, open(
        DATA_FOR_DV_IMPORT_PATH + "swimming-schools.csv", "r"
    ) as swimming_schools_file, open(
        DATA_FOR_DV_IMPORT_PATH + "customers.csv", "w", encoding="utf-8", newline=""
    ) as customers_file:

        first_names = [r["first_name"] for r in csv.DictReader(first_names_file)]
        last_names = [r["last_name"] for r in csv.DictReader(last_names_file)]
        swimming_schools_ids = [r["id"] for r in csv.DictReader(swimming_schools_file)]

        customers_saved = 0

        writer = csv.writer(customers_file)
        writer.writerow(
            "id swimming_school_id first_name last_name email phone is_disabled birth_date is_active".split()
        )

        for i in range(1, n+1):
            first_name=random.choice(first_names)
            last_name=random.choice(last_names)

            # correct polish last-name in case of a woman
            if first_name[-1] == 'a' and last_name[-1] != 'a':
                last_name = last_name[:-1] + 'a'

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

    return customers_saved


if __name__ == "__main__":
    generate_customer_data()
