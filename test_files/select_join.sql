use master
drop database if exists test_join
create database test_join
use test_join
       create table t1(
           pr int primary key,
           unindexed int
       )
       create table t2(
           pr int primary key,
           unindexed int
       )

insert into t1 values(1, 1), (2, 2), (3, 3)
insert into t2 values(1, 1), (2, 1), (3, 2)

select * from t1
join t2 on t1.unindexed = t2.unindexed
