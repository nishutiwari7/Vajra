import mysql.connector

# Function to execute SQL files
def execute_sql_file(filename, connection):
    cursor = connection.cursor()
    try:
        # Open the SQL file and read its content
        with open(filename, 'r') as file:
            sql = file.read()
        
        # Execute SQL commands from the file
        cursor.execute(sql, multi=True)
        connection.commit()  # Commit changes to the database
        print(f"Successfully executed {filename}")
    except Exception as e:
        print(f"Error executing {filename}: {e}")
    finally:
        cursor.close()

# Main function to establish connection and execute SQL files
def main():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="vajra_network"  # Use the database created by the SQL file
        )
        
        # Execute the create, insert, and update SQL files
        execute_sql_file('sql_files/create_database.sql', connection)
        execute_sql_file('sql_files/insert_data.sql', connection)
        execute_sql_file('sql_files/update_data.sql', connection)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
