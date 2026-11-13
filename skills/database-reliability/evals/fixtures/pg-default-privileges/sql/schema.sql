CREATE SCHEMA app AUTHORIZATION app_owner;
CREATE TABLE app.customers (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name text);
CREATE TABLE app.orders (id bigserial PRIMARY KEY, customer_id bigint, total_cents bigint);
CREATE FUNCTION app.order_total(bigint) RETURNS bigint LANGUAGE sql AS 'SELECT total_cents FROM app.orders WHERE id = $1';
