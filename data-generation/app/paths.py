from pathlib import Path

DATA_DICTIONARY = Path("data-dictionary/")
DATA_FOR_DB_IMPORT = Path("data-for-db-import/")

# AI-generated dictionary data to base on
course_descriptions = DATA_DICTIONARY / "course-descriptions.csv"
swimming_school_descriptions = DATA_DICTIONARY / "swimming-schools-descriptions.csv"
swimming_school_names = DATA_DICTIONARY / "swimming-school-names.csv"
cities = DATA_DICTIONARY / "cities.csv"
first_names = DATA_DICTIONARY / "first-names.csv"
last_names = DATA_DICTIONARY / "last-names.csv"

# output files (also used as input for related tables)
swimming_schools = DATA_FOR_DB_IMPORT / "swimming-schools.csv"
instructors = DATA_FOR_DB_IMPORT / "instructors.csv"
courses = DATA_FOR_DB_IMPORT / "courses.csv"
customers = DATA_FOR_DB_IMPORT / "customers.csv"
multisport = DATA_FOR_DB_IMPORT / "multisports.csv"
instructors = DATA_FOR_DB_IMPORT / "instructors.csv"
course_payments = DATA_FOR_DB_IMPORT / "course-payments.csv"
swimming_pools = DATA_FOR_DB_IMPORT / "swimming-pools.csv"
swimming_classes = DATA_FOR_DB_IMPORT / "swimming_classes.csv"
