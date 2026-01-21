import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table() #TODO tables schema

    def create_table(self, table_name, schema):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.cursor.execute(create_table_query)
        self.connection.commit()
    
    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def get_data(self, table_name, conditions=None):
        query = f"SELECT * FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name, updates, conditions):
        update_query = f"UPDATE {table_name} SET {updates} WHERE {conditions}"
        self.cursor.execute(update_query)
        self.connection.commit()

    def delete_data(self, table_name, conditions):
        delete_query = f"DELETE FROM {table_name} WHERE {conditions}"
        self.cursor.execute(delete_query)
        self.connection.commit()