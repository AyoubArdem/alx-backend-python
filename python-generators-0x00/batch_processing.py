import mysql.connector
#methode_1
def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        user="user",
        host="localhost",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    offset = 0

    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        users = cursor.fetchall()
        yield users

        if not users:
            break 
        
        
        offset += batch_size

    cursor.close()
    connection.close()


#methode_2
import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    users=cursor.fetchall()
    batch = []
    for row in users:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    connection.close()
