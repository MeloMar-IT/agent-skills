CREATE TABLE customers (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name text);
CREATE TABLE orders (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL,
  region text,
  amount_cents int,
  created_at timestamptz DEFAULT now()
);
