from psycopg2 import sql, connect

from Intuit.BookExchangeSystem.src.config.config import DB_CONFIG

conn = connect(**DB_CONFIG)


def create_tables():
    with conn.cursor() as cur:
        # users table
        cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255),
                    rating INTEGER DEFAULT 0
                );
            """)
        # books table
        cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    isbn VARCHAR(255),
                    edition VARCHAR(255),
                    condition VARCHAR(255),
                    genre VARCHAR(255),
                    owner_id INTEGER REFERENCES users(id),
                    is_available BOOLEAN DEFAULT TRUE
                );
            """)

        # exchanges table
        cur.execute("""
                CREATE TABLE IF NOT EXISTS exchanges (
                    id SERIAL PRIMARY KEY,
                    requester_id INTEGER REFERENCES users(id),
                    provider_id INTEGER REFERENCES users(id),
                    book_offered_id INTEGER REFERENCES books(id),
                    book_requested_id INTEGER REFERENCES books(id),
                    status VARCHAR(50) DEFAULT 'PENDING',
                    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completion_date TIMESTAMP
                );
            """)

        # notifications table
        cur.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    message TEXT,
                    notif_type VARCHAR(50),
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        # reviews table
        cur.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id SERIAL PRIMARY KEY,
                    reviewer_id INTEGER REFERENCES users(id),
                    reviewee_id INTEGER REFERENCES users(id),
                    rating INTEGER,
                    comment TEXT,
                    exchange_id INTEGER REFERENCES exchanges(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()

create_tables()
def insert_record(table, columns, values, conn):
    with conn.cursor() as cur:
        query = sql.SQL("""
            INSERT INTO {table} ({columns})
            VALUES ({values})
            RETURNING id;
        """).format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cur.execute(query, values)
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id


def get_record_by_id(table, columns, record_id, conn):
    with conn.cursor() as cur:
        query = sql.SQL("""
            SELECT {columns} FROM {table} WHERE id = %s;
        """).format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns))
        )
        cur.execute(query, (record_id,))
        return cur.fetchone()

def update_record(table, columns, values, record_id, conn):
    set_clause = sql.SQL(', ').join(
        sql.SQL("{} = %s").format(sql.Identifier(col)) for col in columns
    )
    query = sql.SQL("""
        UPDATE {table}
        SET {set_clause}
        WHERE id = %s;
    """).format(
        table=sql.Identifier(table),
        set_clause=set_clause
    )
    with conn.cursor() as cur:
        cur.execute(query, values + [record_id])
        conn.commit()

def delete_record(table, record_id, conn):
    with conn.cursor() as cur:
        query = sql.SQL("""
            DELETE FROM {table} WHERE id = %s;
        """).format(
            table=sql.Identifier(table)
        )
        cur.execute(query, (record_id,))
        conn.commit()

def get_records(table, columns, conn, condition=None, condition_values=None):
    with conn.cursor() as cur:
        query = sql.SQL("""
            SELECT {columns} FROM {table} {condition};
        """).format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            condition=sql.SQL(condition) if condition else sql.SQL('')
        )
        cur.execute(query, condition_values if condition_values else ())
        return cur.fetchall()
