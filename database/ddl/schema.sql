-- 1. dim_category
create table dim_category (
	category_id INT primary key,
	category_name VARCHAR (50) not NULL
);
-- Insert static data
insert into dim_category (category_id, category_name) values
(1, 'Income'),
(2, 'Spending');


-- 2. dim_expense
create table dim_expense (
	expense_id INT primary key,
	expense_name VARCHAR(100) not null unique 
);
-- Insert static data
insert into dim_expense (expense_id, expense_name) values 
(0, 'Not Applicable'), --dummy for income
(1, 'Food'),
(2, 'Electricity'),
(3, 'Internet'),
(4, 'Fuel'),
(5, 'Hygiene'),
(6, 'Shopping'),
(7, 'Laundry'),
(8, 'Snacks');


-- 3. dim_source
create table dim_source (
	source_id int primary key,
	source_name varchar(100) not null unique
);
-- Insert static data
insert into dim_source (source_id, source_name) values 
(0, 'Not Applicable'), --dummy for spending
(1, 'Monthly'),
(2, 'Activities'),
(3, 'Others');


-- 4. dim_date
create table dim_date (
    date_id int primary key, --format: YYYYMMDD
    full_date date not null,
    year int not null,
    month_num int not null,
    month_name varchar(20) not null
);

-- 5. fact_transaction
create table fact_transaction (
	transaction_id SERIAL primary key,
	
	-- foreign keys
	date_id INT not null REFERENCES dim_date(date_id),
    category_id INT not null REFERENCES dim_category(category_id),
    expense_id INT not null REFERENCES dim_expense(expense_id),
    source_id INT not null REFERENCES dim_source(source_id),
    
    -- main data
    amount numeric (15, 2) not null,
    description text,
    created_at TIMESTAMP default current_TIMESTAMP
);
