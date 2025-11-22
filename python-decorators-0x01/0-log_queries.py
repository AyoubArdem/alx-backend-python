import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} fetches all users with query: {args[0]}")
        results = func(*args, **kwargs)
        print(f"{func.__name__} gives these results: {results}")
        return results
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users('SELECT * FROM users;')
print(users)
