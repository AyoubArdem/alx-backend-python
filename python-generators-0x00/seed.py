import mysql.connector
import UUID
import csv


def connect_db():
   try:
     return conn=mysql.connector.connect(
         user="root",
         host="localhost",
         password="password"
    )
    except mysql.connector.Error as e:
          print("Connection error:", e)
          return None

def create_database(conn):
    cursor=conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database ALX_prodev created successfully")
    cursor.close()


def connect_to_prodev():
  try:
      return mysql.connector.connect(
            user="root",
            host="localhost",
            password="password",
            database="ALX_prodev"
   )
  except mysql.connector.Error as e:
        print("Error:", e)
        return None

def create_table(conn):
    cursor=conn.cursor()
    cursor.execute( """CREATE TABLE IF NOT EXISTS user_data(
                             user_id VARCHAR(36) PRIMARY KEY,
                             name VARCHAR(255) NOT NULL,
                             email VARCHAR(255) NOT NULL,
                             age DECIMAL NOT NULL
                          );
                    """)
    print("Table user_data created successfully")     
    cursor.close()
                     
                      
def insert_data(conn , filename):
       cursor=conn.cursor()
       with open(filename,'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                        user_id = str(uuid.uuid4())
                        cursor.execute( """ INSERT INTO user_data (user_id,name,email,age)  VALUES (%s,%s,%s,%s) """ , (user_id, row['name'], row['email'], row['age']))
      cursor.commit()
                        
      print("Data inserted successfully")
      cursor.close()





