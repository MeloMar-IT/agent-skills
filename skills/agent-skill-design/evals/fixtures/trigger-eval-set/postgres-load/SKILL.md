---
name: postgres-load
description: Loads CSV files into PostgreSQL with COPY. Use when importing data into a Postgres database table.
---

# Postgres load

Create the table, then run `psql -c "\copy t FROM 'file.csv' CSV HEADER"`.
