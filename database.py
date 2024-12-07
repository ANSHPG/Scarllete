import mysql.connector

def get_db_connection():
    """Establishes and returns a MySQL database connection."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql_server_password",
        database="mysql_server_database_name"
    )
    return connection
