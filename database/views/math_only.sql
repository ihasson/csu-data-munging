CREATE VIEW math_only AS
    SELECT distinct c.* 
    FROM courses c, 
        (select distinct sid from hsdata2) d
    WHERE c.sid = d.sid
      AND (course_name LIKE 'MATH%'
            OR course_name LIKE 'ESM%')
