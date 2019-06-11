create table grades( 
    grade_letter varchar(2),
    grade_value decimal,
    acceptable CHAR(4) );

INSERT INTO grades(grade_letter, grade_value, acceptable)
    VALUES ('A',4.0,'PASS'),
            ('A-',3.7,'PASS'),
            ('B+',3.3,'PASS'),
            ('B',3.0,'PASS'),
            ('B-',2.7,'PASS'),
            ('C+',2.3,'PASS'),
            ('C',2.0,'PASS'),
            ('C-',1.7,'FAIL'),
            ('D+',1.3,'FAIL'),
            ('D',1.0,'FAIL'),
            ('D-',0.7,'FAIL'),
            ('F+',0.3,'FAIL'),
            ('F',0.0,'FAIL'),
            ('CR',NULL,'PASS'),
            ('RP',NULL,'FAIL'),
            ('NC',NULL,'FAIL'),
            ('WU',NULL,'FAIL'); 

    
