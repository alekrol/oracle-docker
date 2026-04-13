CREATE TABLE swimming_school (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(150),
    city VARCHAR2(150),
    capacity NUMBER,
    description VARCHAR2(4000),
    built_date DATE,
    last_renovation_date DATE
);

CREATE TABLE instructor (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(150),
    surname VARCHAR2(150),
    swimming_school_id NUMBER NOT NULL,
    phone_num VARCHAR2(15),
    employment_date DATE,
    salary NUMBER(10, 2),
    CONSTRAINT fk_instr_school FOREIGN KEY (swimming_school_id) REFERENCES swimming_school(id)
);

CREATE TABLE customer (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    swimming_school_id NUMBER NOT NULL,
    name VARCHAR2(150),
    surname VARCHAR2(150),
    email VARCHAR2(150),
    phone VARCHAR2(15),
    is_disabled NUMBER(1) CHECK (is_disabled IN (0, 1)),
    birth_date DATE,
    is_active NUMBER(1) CHECK (is_active IN (0, 1)),
    CONSTRAINT fk_cust_school FOREIGN KEY (swimming_school_id) REFERENCES swimming_school(id)
);

CREATE TABLE multisport (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    discount_percent NUMBER,
    valid_until DATE,
    entries_left NUMBER,
    CONSTRAINT fk_multi_cust FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE swimming_pool (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    swimming_school_id NUMBER NOT NULL,
    max_depth NUMBER,
    min_depth NUMBER,
    is_for_disabled NUMBER(1) CHECK (is_for_disabled IN (0, 1)),
    max_capacity NUMBER,
    pool_length NUMBER,
    is_olympic NUMBER(1) CHECK (is_olympic IN (0, 1)),
    num_of_lanes NUMBER,
    CONSTRAINT fk_pool_school FOREIGN KEY (swimming_school_id) REFERENCES swimming_school(id)
);

CREATE TABLE course (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    description VARCHAR2(4000),
    swimming_school_id NUMBER NOT NULL,
    instructor_id NUMBER NOT NULL,
    date_start DATE,
    date_end DATE,
    price NUMBER(10, 2),
    times_per_week NUMBER,
    max_num_of_participants NUMBER,
    num_of_classes NUMBER,
    is_enrollable NUMBER(1) CHECK (is_enrollable IN (0, 1)),
    is_multisport_accepted NUMBER(1) CHECK (is_multisport_accepted IN (0, 1)),
    CONSTRAINT fk_course_school FOREIGN KEY (swimming_school_id) REFERENCES swimming_school(id),
    CONSTRAINT fk_course_instr FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

CREATE TABLE course_payment (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER NOT NULL,
    amount NUMBER(10, 2),
    created_at DATE DEFAULT SYSDATE,
    course_id NUMBER NOT NULL,
    description VARCHAR2(4000),
    payment_status VARCHAR2(50),
    CONSTRAINT fk_pay_cust FOREIGN KEY (customer_id) REFERENCES customer(id),
    CONSTRAINT fk_pay_course FOREIGN KEY (course_id) REFERENCES course(id)
);

CREATE TABLE swimming_class (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id NUMBER NOT NULL,
    swimming_school_id NUMBER NOT NULL,
    instructor_id NUMBER NOT NULL,
    description VARCHAR2(4000),
    class_type CHAR(2) CHECK (class_type IN ('GR', 'IN', 'PR', 'SP')),
    price NUMBER(10, 2),
    num_of_max_participants NUMBER,
    pool_id NUMBER NOT NULL,
    duration NUMBER,
    time_start TIMESTAMP,
    class_date DATE,
    CONSTRAINT fk_class_course FOREIGN KEY (course_id) REFERENCES course(id),
    CONSTRAINT fk_class_school FOREIGN KEY (swimming_school_id) REFERENCES swimming_school(id),
    CONSTRAINT fk_class_instr FOREIGN KEY (instructor_id) REFERENCES instructor(id),
    CONSTRAINT fk_class_pool FOREIGN KEY (pool_id) REFERENCES swimming_pool(id)
);