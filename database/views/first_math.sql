/* excluding labs. */
/* RP stands for repeat.
 * When a course is retaken for a better grade the previous 
 * grade is changed to RP.
 * Replacement of non-passing grades with RP is not done consistently.
 */
CREATE VIEW  first_math AS 
WITH math_only(
    sid, 
    term,
    course_name,
    units,
    grade
) AS (
    SELECT distinct c.* 
    FROM courses c, 
        (select distinct sid from hsdata2) d
    WHERE c.sid = d.sid
      AND (course_name LIKE 'MATH%'
            OR course_name LIKE 'ESM%')
    )
  SELECT mo.*, grade_value, acceptable
    FROM math_only mo,
        (select sid, MIN(term) as term
           from math_only
          group by sid ) earliest_term,
        grades g
   WHERE mo.sid = earliest_term.sid
     AND mo.term = earliest_term.term
     AND g.grade_letter = mo.grade
     AND course_name  not in ('MATH102L','MATH103L','MATH104L'
       'MATH105L',
         --'MATH131OL',
        --'MATH140OL',
         'MATH150AL',
         'MATH150BL',
         'MATH196HL', --??
         'MATH196LOL',-- ??
         'MATH196NL', --??
         'MATH310L')
         --'MATH331OL',
         --'MATH92OL', 
         --'MATH93OL'
 
