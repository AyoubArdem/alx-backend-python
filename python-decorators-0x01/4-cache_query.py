import sqlite3
import functools
import time

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        else:
            print("Query not cached. Executing...")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn,query):
    cursor=conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
#First call will cach the result
users = fetch_users_with_cache(query="SELECT * FROM users")
#Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
