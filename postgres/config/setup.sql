create schema if not exists raw_schema;
create schema if not exists dw_schema;

create table dw_schema.dim_currency(
    id bigserial primary key,
    currency_code varchar(3) unique,
    currency_name varchar(50)
);