import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Anshu@mysql',
        database='scarllete'
    )
    print("Database connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        connection.close()
