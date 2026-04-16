SELECT 
    c.id AS course_id,
    c.description,
    i.first_name || ' ' || i.last_name AS instructor,
    s.name AS school_name
FROM course c
JOIN instructor i ON c.instructor_id = i.id
JOIN swimming_school s ON c.swimming_school_id = s.id
FETCH FIRST 10 ROWS ONLY;