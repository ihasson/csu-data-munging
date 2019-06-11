create view missing 
as 
select hs.*, c.first_term
from hsdata hs
left join ( Select sid , min(term) first_term from  courses group by sid) c
on c.sid = hs.sid
where c.first_term is null
