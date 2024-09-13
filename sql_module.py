import os
import queue
import threading

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


def connect():
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv('SQL_HOST'),
            user=os.getenv('SQL_USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE'),
            autocommit=os.getenv('AUTOCOMMIT') == 'True'
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
    # TODO: add condition for prof status and do not query this
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


def add_row_to_voicebot_results(response_time, intent_recognized, confidence_score, transcribed_text, bot_response,
                                query_time, query_date, error_code):
    """Add a row of data to the voicebot_results table."""
    query = f"""
    INSERT INTO voicebot_results (response_time, intent_recognized, confidence_score, transcribed_text, bot_response, query_time, query_date, error_code)
    VALUES ({response_time}, '{intent_recognized}', {confidence_score}, '{transcribed_text}', '{bot_response}', '{query_time}', '{query_date}', '{error_code}');
    """
    sql_query(query)
    print("Row added to voicebot_results table.")


def add_row_to_chatbot_results(response_time, intent_recognized, confidence_score, received_text, bot_response,
                               query_time, query_date, error_code):
    """Add a row of data to the chatbot_results table."""
    query = f"""
    INSERT INTO chatbot_results (response_time, intent_recognized, confidence_score, received_text, bot_response, query_time, query_date, error_code)
    VALUES ({response_time}, '{intent_recognized}', {confidence_score}, '{received_text}', '{bot_response}', '{query_time}', '{query_date}', '{error_code}');
    """
    sql_query(query)
    print("Row added to chatbot_results table.")


def add_row_to_suggestions(suggestion, submission_time, submission_date):
    """Add a row of data to the suggestions table."""
    query = f"""
    INSERT INTO suggestions (suggestion, submission_time, submission_date)
    VALUES ('{suggestion}', '{submission_time}', '{submission_date}');
    """
    sql_query(query)


if __name__ == "__main__":
    connect()
    show_tables()
    print("-------------------------------")
    show_columns("admin_control")
    print("-------------------------------")
    # change_value("admin_control", "LCD_state", 0, "ID", 1)

    # print(show_value_as_bool("admin_control", "MOTOR_state", "ID", 1))
    # state = show_value_as_bool("admin_control", "RamiBot_Return", "ID", 1)
    #
    # if state:
    #     print("RamiBot_Return is False")
    # if not state:
    #     print("RamiBot_Return is False")
# table rami_motor_control
