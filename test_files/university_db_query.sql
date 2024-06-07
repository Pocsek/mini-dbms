use University

--no filter, no join
-- select groupId
-- from students;

--no projection, filter 1 indexed equality condition, no join
-- select *
-- from students
-- where GroupId = 531

--no projection, filter 2 indexed equality conditions, no join
-- select *
-- from students
-- where StudName = 'Rosa White' and Email = 'JaneRooney2@email.co'

--no projection, filter 2 indexed equality conditions with different columns, no join
-- select *
-- from marks
-- where StudID = 50 and DiscID = 'OS'

--no projection, filter 1 indexed equality and 1 not-indexed range, with different columns, no join
-- select *
-- from marks
-- where StudID = 50 and Mark > 8;

--# '*' proj
-- select *
-- from students
-- where GroupId = 531 and StudName = 'Nagy Fero'

--# column projections
select StudID, StudName as Fakanal
from students
where GroupId = 233 and StudName = 'Nagy Fero'

--projection, filter 2 equality conditions with different columns, no join
-- select mark
-- from marks
-- where StudID = 50 and DiscID = 'OS';

--no projection, filter multiple equality conditions on same column, no join
-- select *
-- from marks
-- where StudID = 50 or StudID = 41;

--projection, filter multiple equality conditions on same column, no join
-- select StudID, discID, mark
-- from marks
-- where StudID = 50 or StudID = 41;

--no projection, filter range, no join
-- select *
-- from marks
-- where mark > 4 and mark < 7

--projection, filter range, no join
-- select StudID, mark
-- from marks
-- where mark > 4 and mark < 7

--filter not indexed column, 2 joins
-- select StudName, st.GroupId, Email
-- from students st
--     join groups g on st.GroupId = g.GroupId
--     join specialization sp on g.SpecId = sp.SpecID
-- where SpecName = 'Mathematics';

--filter, 2 joins
-- select DName, CreditNr, Mark
-- from students s
--     join marks m on s.StudID = m.StudID
--     join disciplines d on m.discID = d.discID
-- where StudName = 'Rosa White';


--filter range, no join, group
-- select StudID, avg(Mark) as avg_Mark, min(Mark) as min_Mark, max(Mark) as max_Mark
-- from marks
-- where mark > 4 and mark < 7
-- group by StudID;

--filter, 1 join, group
-- select DName, avg(Mark) as avg_Mark
-- from marks m
--     join disciplines d on m.discID = d.discID
-- where mark > 4
-- group by DName;
