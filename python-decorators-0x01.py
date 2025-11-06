import sqlite3
import functools

def log_queries(func):
  @wraps(func)
  def wrapper(*arg,**kwargs):
    print(f"{func.__name__} fetch all users by this query {kwargs}")
    func(*args,**kwargs)
    print(f"{func.__name__} gives these results: {results}")
  return wrapper

@log_queries
def fetch_all_users(query):
  conn=sqlite3.connect('users.db')
  cursor=conn.cursor()
  cursor.execute(query)
  results = cursor.fetchall()
  conn.close()
  return results

users=fetch_all_users('SELECT * FROM users;")
print(users)
