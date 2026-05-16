import mysql.connector

def create_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="db_assignment",
            password="1234"
        )
        cursor = mydb.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_assignment")
        print("Database 'db_assignment' created or verified.")
        cursor.close()
        mydb.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
