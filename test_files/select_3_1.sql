create database test_join
use test_join

create table products (
    product_id int primary key,
    category_id int,
    brand_id int
)

create table categories (
    category_id int primary key
)

create table brands (
    brand_id int primary key
)