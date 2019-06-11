/*sid, term, course, units, grade*/
CREATE TABLE courses (
    sid CHAR(24) NOT NULL,
    term INTEGER NOT NULL,
    course_name VARCHAR(20) NOT NULL,
    units DECIMAL NOT NULL,
    grade VARCHAR(4) NOT NULL 
);

