ALTER TABLE swimming_school
    ADD CONSTRAINT pk_swimming_school PRIMARY KEY (id);

ALTER TABLE instructor
    ADD CONSTRAINT pk_instructor PRIMARY KEY (id);

ALTER TABLE customer
    ADD CONSTRAINT pk_customer PRIMARY KEY (id);

ALTER TABLE multisport
    ADD CONSTRAINT pk_multisport PRIMARY KEY (id);

ALTER TABLE swimming_pool
    ADD CONSTRAINT pk_swimming_pool PRIMARY KEY (id);

ALTER TABLE course
    ADD CONSTRAINT pk_course PRIMARY KEY (id);

ALTER TABLE course_payment
    ADD CONSTRAINT pk_course_payment PRIMARY KEY (id);

ALTER TABLE swimming_class
    ADD CONSTRAINT pk_swimming_class PRIMARY KEY (id);