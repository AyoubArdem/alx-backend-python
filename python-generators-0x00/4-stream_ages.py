import mysql.connector
#methode01
def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:
        yield float(age)
    cursor.close()
    connection.close()

def average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    avg = total / count if count > 0 else 0
    print(f"Average age of users: {avg:.2f}")

#methode02
def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")
    data_user = cursor.fetchall()

    total_age = 0
    for user in data_user:
        total_age += user['age']  

    average_age = total_age / len(data_user) if data_user else 0

    cursor.close()
    connection.close()

    return average_age

#methode03
def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    for user in cursor:
        yield user["age"]

    cursor.close()
    connection.close()

ages = list(stream_user_ages())
average = sum(ages) / len(ages) if ages else 0
