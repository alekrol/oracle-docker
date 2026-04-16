CREATE TABLE swimming_school (
    id NUMBER ,
    name VARCHAR2(150),
    city VARCHAR2(150),
    capacity NUMBER,
    description VARCHAR2(4000),
    built_date DATE,
    last_renovation_date DATE
);

CREATE TABLE instructor (
    id NUMBER ,
    first_name VARCHAR2(150),
    last_name VARCHAR2(150),
    swimming_school_id NUMBER NOT NULL,
    phone_num VARCHAR2(15),
    employment_date DATE,
    salary NUMBER(10, 2)
);

CREATE TABLE customer (
    id NUMBER ,
    swimming_school_id NUMBER NOT NULL,
    first_name VARCHAR2(150),
    last_name VARCHAR2(150),
    email VARCHAR2(150),
    phone VARCHAR2(15),
    is_disabled NUMBER(1) CHECK (is_disabled IN (0, 1)),
    birth_date DATE,
    is_active NUMBER(1) CHECK (is_active IN (0, 1))
);

CREATE TABLE multisport (
    id NUMBER ,
    customer_id NUMBER NOT NULL,
    discount_percent NUMBER,
    valid_until DATE,
    entries_left NUMBER
);

CREATE TABLE swimming_pool (
    id NUMBER ,
    swimming_school_id NUMBER NOT NULL,
    max_depth NUMBER,
    min_depth NUMBER,
    is_for_disabled NUMBER(1) CHECK (is_for_disabled IN (0, 1)),
    max_capacity NUMBER,
    length NUMBER,
    is_olympic NUMBER(1) CHECK (is_olympic IN (0, 1)),
    num_of_lanes NUMBER
);

CREATE TABLE course (
    id NUMBER ,
    description VARCHAR2(4000),
    swimming_school_id NUMBER NOT NULL,
    instructor_id NUMBER NOT NULL,
    date_start DATE,
    date_end DATE,
    price NUMBER(10, 2),
    times_per_week NUMBER,
    max_num_of_participants NUMBER,
    num_of_classes NUMBER,
    is_multisport_accepted NUMBER(1) CHECK (is_multisport_accepted IN (0, 1)),
    is_enrollable NUMBER(1) CHECK (is_enrollable IN (0, 1))
);

CREATE TABLE course_payment (
    id NUMBER ,
    course_id NUMBER NOT NULL,
    customer_id NUMBER NOT NULL,
    status VARCHAR2(50),
    created_at DATE DEFAULT SYSDATE,
    description VARCHAR2(4000),
    amount_paid NUMBER(10, 2)
);

CREATE TABLE swimming_class (
    id NUMBER ,
    course_id NUMBER NOT NULL,
    swimming_school_id NUMBER NOT NULL,
    instructor_id NUMBER NOT NULL,
    description VARCHAR2(4000),
    class_type CHAR(2),
    price NUMBER(10, 2),
    num_of_max_participants NUMBER,
    pool_id NUMBER NOT NULL,
    duration NUMBER,
    time_start TIMESTAMP,
    class_date DATE
);