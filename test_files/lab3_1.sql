use master
drop database if exists Lab3
create database Lab3
use Lab3

create table t1 (
    id   int primary key identity(1,2),
    name varchar,
    age  int check (age > 18)
)

create table t2 (
    id   int primary key identity,
    age int references t1(age),
    cnp varchar unique
)

