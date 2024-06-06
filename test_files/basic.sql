drop database if exists test;
create database test;
use test;
create table test_table (
    id int primary key identity,
    name varchar
);

insert into test_table (name) values ('test'), ('test2');
delete from test_table where id = 1;

