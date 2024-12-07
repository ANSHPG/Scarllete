import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anshu@mysql",
    database="scarllete"
)

try:
    # Create a cursor to execute the stored procedure
    cursor = connection.cursor()

    # Call the stored procedure with test values
    cursor.callproc('insert_expense_and_update_category', (1, 150.00, 1))

    # Commit the transaction
    connection.commit()

    print("Test insertion completed successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    connection.close()
