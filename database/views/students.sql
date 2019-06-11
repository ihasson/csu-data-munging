CREATE VIEW hsdata0 AS 
SELECT t.*, cohort, term
FROM 
 tmp_hsdata t
join cohort c
on c.sid = t.sid
WHERE c.cohort = 'FTF'
AND   CAST(c.term as Integer) >= 2067
