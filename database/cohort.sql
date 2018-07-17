CREATE TABLE cohort (
    sid CHAR(24) NOT NULL,
    cohort VARCHAR(10) NOT NULL,
    term CHAR(4) NOT NULL,
    PRIMARY KEY (sid) 
);   


CREATE TABLE exams (
    sid CHAR(24) NOT NULL,
    exam VARCHAR(11) NOT NULL,
    exam_subject VARCHAR(1000) NOT NULL,
    score INTEGER NOT NULL,
    exam_date DATE NOT NULL,
    FOREIGN KEY (sid) REFERENCES cohort(sid)
);
