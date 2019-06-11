
CREATE TABLE exams (
    sid CHAR(24) NOT NULL,
    exam VARCHAR(11) NOT NULL,
    exam_subject VARCHAR(1000) NOT NULL,
    score DECIMAL NOT NULL,
    exam_date DATE NOT NULL,
    FOREIGN KEY (sid) REFERENCES cohort(sid)
);
