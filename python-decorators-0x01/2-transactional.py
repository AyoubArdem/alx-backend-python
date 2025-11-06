import functools
import sqlite3

def transactional(func):
  @functools.wraps(func)
  def wrapper(conn,*args,**kwargs):
     try:
          conn.execute("Begin")
          result=func(conn,*args,**kwargs)
          conn.commit()
          return result
     except EXCEPTION as e:
           conn.rollback()
           raise e
  return wrapper


@with_db_connection
@transactional
def update_user_email(conn,user_id,new_email):
    cursor=conn.cursor()
    cursor.execute("UPDATE FROM user SET email=? WHERE user_id=?",(new_email,user_id))

update_user_email(
    user_id=1,
    new_email='Crawford_Cartwright@hotmail.com'
)
