import mysql.connector
global sql_connection

sql_connection = {
    "host": "localhost",  
    "user": "root",       
    "password": "Anshu@mysql",  
    "database": "scarlette" 
}

#insert values into keys 
def insert_values(category, amount):
    try:
        cursor = sql_connection.cursor()

        cursor.callproc()