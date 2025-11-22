import functools
import time
import sqlite3

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(conn)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    time.sleep(delay)
            print("All retries failed.")
            raise last_exception
        return wrapper
    return decorator
@with_db_connection
@retry_on_failure(retries=3,delay=2)

def fetch_users_with_retry(conn):
     cursor=conn.cursor()
     cursor.execute("SELECT * FROM users;")
     return cursor.fetchall()

users=fetch_users_with_retry()
print(users)
