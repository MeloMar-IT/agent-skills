def set_tenant(conn, tenant):
    conn.execute("SET search_path TO " + tenant)  # session level


def with_statement_timeout(conn):
    with conn.transaction():
        conn.execute("SET LOCAL statement_timeout = '5s'")
        return conn.execute("SELECT count(*) FROM orders").fetchone()


def run_singleton_job(conn, job):
    if not conn.execute("SELECT pg_try_advisory_lock(42)").fetchone()[0]:
        return
    for step in job:
        with conn.transaction():
            step(conn)
    conn.execute("SELECT pg_advisory_unlock(42)")


def charge_once(conn, order_id):
    with conn.transaction():
        conn.execute("SELECT pg_advisory_xact_lock(%s)", (order_id,))
        conn.execute("UPDATE orders SET charged = true WHERE id = %s", (order_id,))


def listen_for_invalidations(conn):
    conn.execute("LISTEN cache_invalidate")
    return conn.notifies()


def bulk_price_lookup(conn, ids):
    conn.execute("PREPARE price_q (bigint) AS SELECT price FROM items WHERE id = $1")
    return [conn.execute("EXECUTE price_q(%s)", (i,)).fetchone() for i in ids]


def export_report(conn):
    conn.execute("DECLARE rpt CURSOR WITH HOLD FOR SELECT * FROM report_rows")
    return conn.execute("FETCH 100 FROM rpt").fetchall()


def stage_import(conn, rows):
    with conn.transaction():
        conn.execute("CREATE TEMP TABLE stage (id bigint, v text) ON COMMIT DROP")
        conn.executemany("INSERT INTO stage VALUES (%s, %s)", rows)
        conn.execute("INSERT INTO imports SELECT * FROM stage")
