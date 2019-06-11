select count(c.sid)
from
       (select sid from math_only where course_name = 'MATH140') s,
       (select sid from math_only where course_name = 'MATH150A') c
where c.sid = s.sid ;
