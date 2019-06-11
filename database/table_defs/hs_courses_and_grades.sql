CREATE TABLE hs_courses_and_grades (
    sid CHAR(24) NOT NULL,
    application_nbr CHAR(8) NOT NULL,
    hs_subject  INTEGER,
    hs_crs_nbr INTEGER,
    hs_grade_level INTEGER,
    descr VARCHAR(21844),
    fall_gr VARCHAR(4),
    spr_gr VARCHAR(4),
    sum_gr VARCHAR(4),
    honors VARCHAR(1),
    sum2_gr VARCHAR(4),
    cman CHAR(4),
    high_school TEXT,
    course_source VARCHAR(30),
    FOREIGN KEY (sid) REFERENCES cohort(sid)
);
