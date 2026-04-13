from datetime import date, timedelta
import random
import csv
from . import paths

MAILS = "gmail o2 yahoo bing wp outlook company".split()
DOMAINS = "pl en com us gov eu de fr io".split()
PHONE_PREFIXES = "+48 +212 +12 +10 +42 +13 +65 +11".split()


def random_date(start: date, end: date) -> date:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


# replace polish characters with international ones
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

    return "".join(PL_TO_ASCII.get(c, c) for c in s)


def generate_number() -> str:
    return random.choice(PHONE_PREFIXES) + "".join(
        [str(random.randint(0, 9)) for _ in range(9)]
    )


def generate_mail(first_name: str, last_name: str) -> str:
    return serialize_str(
        str(first_name[:3]).lower()
        + "."
        + str(last_name[:3]).lower()
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


def generate_names_and_surnames(n) -> list[tuple[str, str]]:
    names = []

    with open(paths.first_names, "r") as first_names_file, open(
        paths.last_names, "r"
    ) as last_names_file:
        first_names = [r["first_name"] for r in csv.DictReader(first_names_file)]
        last_names = [r["last_name"] for r in csv.DictReader(last_names_file)]

        for _ in range(n):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            if first_name[-1] == "a" and last_name[-1] != "a":
                last_name = last_name[:-1] + "a"

            names.append((first_name, last_name))

    return names
