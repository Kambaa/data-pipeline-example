import os
import time
from faker import Faker
from typing import List, Tuple, Dict, Any
from psycopg_pool import ConnectionPool
from psycopg import sql, OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")
DB_CONN_RETRIES = int(os.getenv("DB_CONN_RETRIES", "30"))  # default 30 retries
DB_CONN_DELAY = float(os.getenv("DB_CONN_DELAY", "2"))    # default 2 seconds delay
fake = Faker()

def wait_for_db_conn(retries=DB_CONN_RETRIES, delay=DB_CONN_DELAY):
    for attempt in range(1, retries + 1):
        try:
            pool = ConnectionPool(conninfo=DATABASE_URL, open=True)
            # Test connection
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
            print("Database connection successful.")
            return pool
        except OperationalError as e:
            print(f"DB connection attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    raise Exception(f"Could not connect to the database after {retries} attempts.")

def setup_table(pool):
    print("Setting up the table...")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                 CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    person_name TEXT,
                    company_name TEXT,
                    iban TEXT,
                    phone_number TEXT,
                    identification_number TEXT,
                    email TEXT,
                    dob DATE,
                    address TEXT,
                    zip_code TEXT,
                    job_title TEXT
                    );
            """)
            conn.commit()
    print("Table ready.")

def insert_one(pool):
    print("Inserting one row...")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            query = sql.SQL("INSERT INTO test_table (person_name, company_name) VALUES (%s, %s)")
            cur.execute(query, ("John Doe", "Acme Corp"))
            conn.commit()
    print("Inserted 1 row.")

def bulk_insert(pool, rows: List[Tuple]):
    query = (
        "INSERT INTO test_table "
        "(person_name, company_name, iban, phone_number, identification_number, email, dob, address, zip_code, job_title) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, rows)
        conn.commit()
    print(f"Inserted {len(rows)} rows")




def generate_clean_record() -> Dict[str, Any]:
    return {
        "person_name": fake.name(),
        "company_name": fake.company(),
        "iban": fake.iban(),
        "phone_number": fake.phone_number(),
        "identification_number": str(fake.random_number(digits=10, fix_len=True)),
        "email": fake.email(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "address": fake.address().replace("\n", ", "),
        "zip_code": fake.postcode(),
        "job_title": fake.job(),
    }
def dict_to_tuple(d: Dict[str, Any]) -> Tuple:
    return (
        d["person_name"],
        d["company_name"],
        d["iban"],
        d["phone_number"],
        d["identification_number"],
        d["email"],
        d["dob"],
        d["address"],
        d["zip_code"],
        d["job_title"],
    )


def main():
    print("Starting app... waiting for DB connection.")
    pool = wait_for_db_conn()
    setup_table(pool)
    # insert_one(pool)
    records = [generate_clean_record() for _ in range(500)]
    rows = [dict_to_tuple(r) for r in records]
    bulk_insert(pool,rows)
    print("Done.")

if __name__ == "__main__":
    main()
