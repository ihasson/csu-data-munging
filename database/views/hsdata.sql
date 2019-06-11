CREATE VIEW hsdata1 AS 
SELECT t.*
FROM 
 tmp_hsdata t,
 cohort c
WHERE c.sid = t.sid
AND   c.cohort = 'FTF'
AND   CAST(c.term as Integer) >= 2067
