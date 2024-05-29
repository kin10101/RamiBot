import mysql.connector


def connect():
    return mysql.connector.connect(
        host="airhub-soe.apc.edu.ph",
        user="marj",
        password="RAMIcpe211",
        database="ramibot"
    )


def disconnect():
    conn = connect()
    conn.close()


def check_connection():
    conn = connect()
    print(conn.is_connected())
    conn.close()


def sql_query(query):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
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
    query = f";"
    sql_query(query)


if __name__ == "__main__":
    connect()
    show_tables()
    print("-------------------------------")
    show_columns("admin_control")

    change_value("admin_control", "Ramibot_Return", "2", "ID", "1")
    column_data = get_column_data("admin_control", "")
    print(column_data)


#table rami_motor_control
