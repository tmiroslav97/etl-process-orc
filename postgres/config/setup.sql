create schema if not exists raw_schema;
create schema if not exists dw_schema;

create table dw_schema.dim_currency(
    id bigserial primary key,
    currency_code varchar(3) unique,
    currency_name varchar(50)
);

create table dw_schema.fact_currency_rate(
    id bigserial primary key,
    date_rate date,
    avg_rate float,
    end_of_day_rate float,
    currency_id bigint,
    constraint curr_fk foreign key (currency_id) references dw_schema.dim_currency(id)
);