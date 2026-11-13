ALTER TABLE orders ADD COLUMN public_id uuid DEFAULT gen_random_uuid();
ALTER TABLE orders ADD COLUMN status text NOT NULL DEFAULT 'new';
CREATE UNIQUE INDEX orders_public_id_key ON orders (public_id);
ALTER TABLE orders ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers (id);
ALTER TABLE orders ALTER COLUMN region SET NOT NULL;
