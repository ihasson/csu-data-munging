/* this is again for hs data only */
CREATE VIEW valid_grade_lines AS 
WITH vg( grade_letter) 
as (
    select grade_letter from grades where 
    grade_letter not in ('WU','NC','RP','CR')
),
valid_courses(
     sid,
     valid_count)
AS (
     SELECT sid, COUNT(line_id) as valid
     from (
     SELECT DISTINCT hs.* 
     FROM hsdata hs, grades grd
     WHERE hs.line_id not in (select line_id from middle)
     AND (fall_gr in (select * from vg) OR fall_gr is NULL)
     AND (spr_gr in (select * from vg) OR spr_gr is NULL)
     AND (sum_gr in (select * from vg) OR sum_gr is NULL)
     AND (sum2_gr in (select * from vg) OR sum2_gr is NULL)
     AND (fall_gr IS NOT NULL OR
         spr_gr IS NOT NULL OR
             sum_gr IS NOT NULL OR
                 sum2_gr IS NOT NULL)) t
                 group by sid
),
all_courses(
    sid,
    courses_total)
AS(
    Select sid , count(sid)
    From hsdata
    group by sid)
SELECT vc.sid, vc.valid_count, ac.courses_total,
       (cast(vc.valid_count as decimal) /cast( ac.courses_total as decimal)) as percent_valid
FROM valid_courses vc,
     all_courses ac
WHERE vc.sid = ac.sid
