import random
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
import class_desc as c

random.seed(42)

@dataclass
class Multisport:
    id: int
    customer: 'Customer'
    discount_percent: int
    valid_until: date
    entries_left: int

@dataclass
class Customer:
    id: int
    swimming_school: 'SwimmingSchool'
    name: str
    surname: str
    email: str
    phone: str
    is_disabled: bool
    birth_date: date
    is_active: bool

@dataclass
class SwimmingSchool:
    id: int
    name: str
    city: str
    capacity: int
    description: str
    built_date: date
    last_renovation_date: date

@dataclass
class Instructor:
    id: int
    name: str
    surname: str
    swimming_school: SwimmingSchool
    phone_num: str
    employment_date: date
    salary: int

@dataclass
class Course:
    id: int
    description: str
    swimming_school: SwimmingSchool
    instructor: Instructor
    date_start: date
    date_end: date
    price: int
    times_per_week: int
    max_num_of_participants: int
    num_of_classes: int
    is_enrollable: bool
    is_multisport_accepted: bool

@dataclass
class SwimmingPool:
    id: int
    swimming_school: SwimmingSchool
    max_depth: int # cm
    min_depth: int # cm
    is_for_disabled: bool
    max_capacity: int
    length: int # m
    is_olympic: bool
    num_of_lanes: int

@dataclass
class CoursePayment:
    class Status(Enum):
        PAID = 'PAID'
        PENDING = 'PENDING'
        NOT_PAID = 'NOT_PAID'

    id: int
    customer: Customer
    amount: int
    created_at: date
    course: Course
    description: str
    status: Status

@dataclass
class SwimmingClass:
    class ClassType(Enum):
        ADV = 'ADVANCED'
        BEG = 'BEGINNER'
        INT = 'INTERMEDIATE'
        DIS = 'DISABLED'
        CHI = 'CHILDREN'
        MIX = 'MIX'

    class ClassDescription(Enum):
        ADV = c.ADV_DESC
        INT = c.INT_DESC
        BEG = c.BEG_DESC
        MIX = c.MIX_DESC
        CHI = c.CHI_DESC
        DIS = c.DIS_DESC

    class_map = {
        ClassType.ADV: ClassDescription.ADV,
        ClassType.BEG: ClassDescription.BEG,
        ClassType.INT: ClassDescription.INT,
        ClassType.MIX: ClassDescription.MIX,
        ClassType.DIS: ClassDescription.DIS,
        ClassType.CHI: ClassDescription.CHI
    }
    
    course: Course
    swimming_school: SwimmingSchool
    instructor: Instructor
    description: str
    class_type: ClassType
