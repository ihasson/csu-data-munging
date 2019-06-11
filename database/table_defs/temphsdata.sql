
CREATE TABLE tmp_hsdata (
    sid CHAR(24) NOT NULL,
    application_nbr CHAR(8) NOT NULL,
    hs_subject TEXT, --INTEGER,
    hs_crs_nbr TEXT, --INTEGER,
    hs_grade_level TEXT, --INTEGER
    descr TEXT,
    fall_gr TEXT, --VARCHAR(4),
    spr_gr TEXT, --VARCHAR(4),
    sum_gr TEXT, --VARCHAR(4),
    honors TEXT, --VARCHAR(1),
    sum2_gr TEXT, --VARCHAR(4),
    cman TEXT, --CHAR(4),
    high_school TEXT,
    course_source TEXT, --VARCHAR(30),
    line_id INTEGER,
    PRIMARY KEY (line_id)
    --FOREIGN KEY (sid) REFERENCES cohort(sid)
    --CONSTRAINT
      --   CHECK ([application_nbr] LIKE REPLICATE('[0-9]', 8))
);
