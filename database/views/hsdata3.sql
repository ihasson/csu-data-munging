CREATE VIEW hsdata3 AS 
SELECT DISTINCT t.*
FROM 
 tmp_hsdata t,
 cohort c,
 (select distinct sid from courses) cc,
 (select distinct sid from majors) m
WHERE c.sid = t.sid
AND   c.cohort = 'FTF'
AND   CAST(c.term as Integer) >= 2067
AND   cc.sid = t.sid
AND   cc.sid = c.sid
AND   m.sid = c.sid
AND   m.sid = t.sid
AND   m.sid = cc.sid
