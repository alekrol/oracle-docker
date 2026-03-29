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


def generate_swimming_school_data() -> int:
    header = "id name city capacity description built_date last_renovation_date".split()

    def swimming_school_to_row(s:SwimmingSchool)->list[SwimmingSchool]:
        return [
            s.id,
            s.name,
            s.city,
            s.capacity,
            s.description,
            s.built_date,
            s.last_renovation_date
        ]
    
    def random_date(start: date, end: date) -> date:
        delta = end - start
        return start + timedelta(days=random.randint(0, delta.days))

    with open(EXAMPLE_DATA_PATH + "cities.csv", "r") as cities, open(
        EXAMPLE_DATA_PATH + "swimming-schools-descriptions.csv", "r"
    ) as descriptions, open(
        EXAMPLE_DATA_PATH + "swimming-school-names.csv", "r"
    ) as names, open(
        DATA_FOR_DV_IMPORT_PATH + "swimming-schools.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as schools:

        writer = csv.writer(schools)
        writer.writerow(header)

        saved_schools = 0

        names = [row["name"] for row in csv.DictReader(names)]
        descriptions = [row["description"] for row in csv.DictReader(descriptions)]
        cities = [row["city"] for row in csv.DictReader(cities)]

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

if __name__ == '__main__':
    generate_swimming_school_data()
