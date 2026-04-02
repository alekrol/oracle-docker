from dataclasses import dataclass, astuple
from datetime import date
from enum import Enum

@dataclass
class Multisport:
    id: int
    customer_id: int
    discount_percent: int
    valid_until: date
    entries_left: int

    def field_values_to_list(self):
        return list(astuple(self))

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

    def field_values_to_list(self):
        return list(astuple(self))

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
    is_multisport_accepted: bool
    is_enrollable: bool | None = True # for now I dont know how to do it

    def field_values_to_list(self):
        return list(astuple(self))

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
    course_id: int
    swimming_school_id: int
    instructor_id: int
    description: str
    class_type: str
