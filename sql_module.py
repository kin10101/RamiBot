import mysql.connector
from mysql.connector import Error


def connect():
    try:
        connection = mysql.connector.connect(
            host="airhub-soe.apc.edu.ph",
            user="marj",
            password="RAMIcpe211",
            database="ramibot",
            autocommit=True
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        pass


def disconnect():
    conn = connect()
    conn.close()


def check_connection():
    conn = connect()
    print(conn.is_connected())
    conn.close()


def sql_query(query):
    try:
        conn = connect()
        if conn is None:
            raise Exception("Failed to connect to the database")

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: {e}")
        return None


def show_tables():
    tables = sql_query("SHOW TABLES;")
    for table in tables:
        print(table[0])


def show_columns(table):
    columns = sql_query(f"SHOW COLUMNS FROM {table};")
    for column in columns:
        print(column[0])


def get_column_data(table, column):
    """Get all data from a column in a table."""
    query = f"SELECT {column} FROM {table} WHERE {column} IS NOT NULL AND {column} != '';"
    results = sql_query(query)
    # Extract the first element of each tuple in the results
    column_data = [result[0] for result in results if result[0] != 'NULL']

    return column_data


def insert_data(table, columns, values):
    """Insert data into a table."""
    columns_str = ", ".join(columns)
    values_str = ", ".join([f"'{value}'" for value in values])
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({values_str});"
    sql_query(query)


def change_value(table, column, value, condition_column, condition_value):
    """Change a value in a table."""
    query = f"UPDATE {table} SET {column} = '{value}' WHERE {condition_column} = '{condition_value}';"
    sql_query(query)


def show_value(table, column, condition_column, condition_value):
    query = f"SELECT {column} FROM {table} WHERE {condition_column} = {condition_value}"
    result = sql_query(query)
    return result


if __name__ == "__main__":
    connect()
    # show_tables()
    # print("-------------------------------")
    # show_columns("admin_control")
    # print("-------------------------------")
    print(show_value("admin_control", "MOTOR_state", "ID", 1))

# table rami_motor_control
