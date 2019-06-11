CREATE VIEW hsdata2 AS 
SELECT  t.*
FROM 
 tmp_hsdata t,
 cohort c ,
 (SELECT distinct sid from courses) cc  
WHERE
c.sid = cc.sid and t.sid = cc.sid
AND   c.cohort = 'FTF'
AND   CAST(c.term as Integer) >= 2067
AND   c.sid = cc.sid and t.sid = cc.sid

