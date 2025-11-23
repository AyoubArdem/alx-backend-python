import sqlite3

class ExecuteQuery:
    """Reusable context manager that executes a given query."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params 
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.commit()
            self.connection.close()


if __name__ == "__main__":
    with ExecuteQuery("my_database.db", "SELECT * FROM users WHERE age > ?", (25,)) as result:
        for row in result:
            print(row)
