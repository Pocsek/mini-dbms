use master;
drop database if exists test_db;
create database test_db;
use test_db;
create table parent_table (
    id int primary key
);
create table child_table (
    id int primary key,
    parent_id int,
    foreign key (parent_id) references parent_table(id)
);
insert into parent_table values (1), (2), (3);
insert into child_table values (1, 1), (2, 2), (3, 3);
delete from parent_table where id = 1;