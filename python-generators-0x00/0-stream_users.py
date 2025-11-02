import mysql.connector

def stream_users():
   connection=mysql.connector.connect(
         user:"root",
         host:"localhost",
         password:"password",
         database="ALX_prodev"
   )
   cursor=connection.cursor(dictionary=True)
   for row in cursor.execute('SELECT * FROM user_data;):
                  yield row
    cursor.close()
    conn.close()
