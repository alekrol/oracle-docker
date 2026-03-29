from dataclasses import dataclass
from datetime import date
from enum import Enum
from .class_desc import ADV_DESC, INT_DESC, BEG_DESC, MIX_DESC, DIS_DESC, CHI_DESC


@dataclass
class Multisport:
    id: int
    customer_id: int
    discount_percent: int
    valid_until: date
    entries_left: int

@dataclass
class Customer:
    id: int
    swimming_school_id: int
    first_name: str
    last_name: str
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
    first_name: str
    last_name: str
    swimming_school_id: int
    phone_num: str
    employment_date: date
    salary: int

@dataclass
class Course:
    id: int
    description: str
    swimming_school_id: int
    instructor_id: int
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
    swimming_school_id: int
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
        ADV = ADV_DESC
        INT = INT_DESC
        BEG = BEG_DESC
        MIX = MIX_DESC
        CHI = CHI_DESC
        DIS = DIS_DESC

    class_map = {
        ClassType.ADV: ClassDescription.ADV,
        ClassType.BEG: ClassDescription.BEG,
        ClassType.INT: ClassDescription.INT,
        ClassType.MIX: ClassDescription.MIX,
        ClassType.DIS: ClassDescription.DIS,
        ClassType.CHI: ClassDescription.CHI
    }

    course_id: int
    swimming_school_id: int
    instructor_id: int
    description: str
    class_type: ClassType
