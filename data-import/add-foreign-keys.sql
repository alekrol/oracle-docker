ALTER TABLE instructor
    ADD CONSTRAINT fk_instructor_swimming_school
    FOREIGN KEY (swimming_school_id)
    REFERENCES swimming_school(id);

ALTER TABLE customer
    ADD CONSTRAINT fk_customer_swimming_school
    FOREIGN KEY (swimming_school_id)
    REFERENCES swimming_school(id);

ALTER TABLE multisport
    ADD CONSTRAINT fk_multisport_customer
    FOREIGN KEY (customer_id)
    REFERENCES customer(id);

ALTER TABLE swimming_pool
    ADD CONSTRAINT fk_swimming_pool_swimming_school
    FOREIGN KEY (swimming_school_id)
    REFERENCES swimming_school(id);

ALTER TABLE course
    ADD CONSTRAINT fk_course_swimming_school
    FOREIGN KEY (swimming_school_id)
    REFERENCES swimming_school(id);

ALTER TABLE course
    ADD CONSTRAINT fk_course_instructor
    FOREIGN KEY (instructor_id)
    REFERENCES instructor(id);

ALTER TABLE course_payment
    ADD CONSTRAINT fk_course_payment_course
    FOREIGN KEY (course_id)
    REFERENCES course(id);

ALTER TABLE course_payment
    ADD CONSTRAINT fk_course_payment_customer
    FOREIGN KEY (customer_id)
    REFERENCES customer(id);

ALTER TABLE swimming_class
    ADD CONSTRAINT fk_swimming_class_course
    FOREIGN KEY (course_id)
    REFERENCES course(id);

ALTER TABLE swimming_class
    ADD CONSTRAINT fk_swimming_class_swimming_school
    FOREIGN KEY (swimming_school_id)
    REFERENCES swimming_school(id);

ALTER TABLE swimming_class
    ADD CONSTRAINT fk_swimming_class_instructor
    FOREIGN KEY (instructor_id)
    REFERENCES instructor(id);

ALTER TABLE swimming_class
    ADD CONSTRAINT fk_swimming_class_pool
    FOREIGN KEY (pool_id)
    REFERENCES swimming_pool(id);