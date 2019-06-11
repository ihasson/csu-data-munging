CREATE VIEW placement_outcomes AS
select math_cat, mt.mathlvl, acceptable, count(fm.sid) 
from math_category mc, first_math fm, mathtype mt 
where mc.sid = fm.sid and mt.course_name = fm.course_name 
group by acceptable,math_cat,mathlvl;

