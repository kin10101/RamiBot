import queue
import threading

import mysql.connector
from mysql.connector import Error


def connect():
    try:
        connection = mysql.connector.connect(
            # host="airhub-soe.apc.edu.ph",
            # user="marj",
            # password="RAMIcpe211",
            # database="ramibot",
            # autocommit=True

            # database access for local testing
            host="localhost",
            user="kin",
            password="asdf",
            database="ramibot_local",
            autocommit=True
        )
        if connection.is_connected():
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


# def query(query):
#     try:
#         conn = connect()
#         if conn is None:
#             raise Exception("Failed to connect to the database")
#
#         cursor = conn.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"Error: {e}")
#         return None


def execute_query(sql_query, result_queue):
    try:
        conn = connect()
        if conn is None:
            raise Exception("Failed to connect to the database")

        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        result_queue.put((result, None))  # Put the result in the queue
    except Error as e:
        print(f"Error: {e}")
        result_queue.put((None, e))  # Put the error in the queue


def sql_query(query):
    i = 1
    result_queue = queue.Queue()
    thread = threading.Thread(target=execute_query, args=(query, result_queue))
    thread.start()
    result, error = result_queue.get()  # Wait for the result

    if error:
        print(f"Query error: {error}")
        return None

    return result


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


def show_value_as_bool(table, column, condition_column, condition_value):
    query = f"SELECT {column} FROM {table} WHERE {condition_column} = {condition_value}"
    result = sql_query(query)
    if result and result[0]:
        return bool(int(result[0][0]))
    else:
        return None


if __name__ == "__main__":
    connect()
    show_tables()
    print("-------------------------------")
    show_columns("admin_control")
    print("-------------------------------")
    change_value("admin_control", "LCD_state", 0, "ID", 1)
    # print(show_value_as_bool("admin_control", "MOTOR_state", "ID", 1))
    # state = show_value_as_bool("admin_control", "RamiBot_Return", "ID", 1)
    #
    # if state:
    #     print("RamiBot_Return is False")
    # if not state:
    #     print("RamiBot_Return is False")
# table rami_motor_control
