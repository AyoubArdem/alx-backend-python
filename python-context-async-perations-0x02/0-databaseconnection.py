import sqlite3

class DatabaseConnection:
    """Class-based context manager for handling DB connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection."""
        if self.connection:
            self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    with DatabaseConnection("my_database.db") as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, age INTEGER)")
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)


