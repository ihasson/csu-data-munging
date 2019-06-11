/* for highschool grades only, and doesn't do the entire thing */
WITH fall( 
    line_id, fall_gr, fall_val)
AS (
    SELECT distinct line_id, fall_gr, g.grade_value
    FROM   hsdata2, grades g
    WHERE  g.grade_letter = fall_gr
),
spring (
    line_id, spr_gr, spr_val)
AS ( 
    SELECT distinct line_id, spr_gr, g.grade_value
    FROM   hsdata2, grades g
    WHERE  g.grade_letter = spr_gr
),
summer (
    line_id, sum_gr, sum_val)
AS ( 
    SELECT distinct line_id, sum_gr, g.grade_value
    FROM   hsdata2, grades g
    WHERE  g.grade_letter = sum_gr
),
summer2 (
    line_id, sum2_gr, sum2_val)
AS ( 
    SELECT distinct line_id, sum2_gr, g.grade_value
    FROM   hsdata2, grades g
    WHERE  g.grade_letter = sum2_gr
)
SELECT hs.line_id, fall.fall_val, spr_val, sum_val, sum2_val
FROM (select distinct line_id from hsdata2) hs
left join fall on fall.line_id = hs.line_id  
left join spring on spring.line_id = hs.line_id
left join summer on summer.line_id = hs.line_id
left join summer2 on summer2.line_id = hs.line_id
