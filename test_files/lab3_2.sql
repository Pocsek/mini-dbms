use Lab3

-- insert into t1 values ('John', 20), ('Jane', 12) -- check rossz
-- insert into t1 values ('John', 20), ('Jane', 68) -- check jo
-- insert into t2 values (20, '12'), (2, '12')  -- unique rossz
-- insert into t1 values ('John', 21), ('Jane', 68) -- check jo
-- insert into t2 values (20, '1'), (21, '2')  -- unique jo, foreign key rossz
-- insert into t2 values (20, '1'), (20, '2')  -- unique jo, foreign key jo


-- create index idx_t1_name on t1(name)
-- drop table t1
-- drop table t2
-- drop table t1
