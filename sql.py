import mysql.connector

def connect():
    return mysql.connector.connect(
        host="airhub-soe.apc.edu.ph",
        user="marj",
        password="RAMIcpe211",
        database="ramibot"
    )


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
    query = f"SELECT {column} FROM {table};"
    results = sql_query(query)
    # Extract the first element of each tuple in the results
    column_data = [result[0] for result in results]
    return column_data

def speak(text, lang='en'):
    # Create a gTTS object
    tts = gTTS(text, lang=lang)

    # Save the speech as an audio file
    tts.save("output.mp3")

    # Initialize the audio player
    pygame.mixer.init()
    sound = pygame.mixer.Sound("output.mp3")

    # Play the speech
    sound.play()
    # Wait for the speech to finish
    pygame.time.delay(int(sound.get_length() * 1000))
    pygame.quit()

#INSERT INTO VALUES
if __name__ == "__main__":
    connect()
    show_tables()
    show_columns("programs_img")

    column_data = get_column_data("text_to_voice_announcements", "announcement_name")
    print(column_data)

    import pygtts
    import random
    def random_item(mytuple):
        return random.choice(mytuple)
    text = random_item(column_data)

    from gtts import gTTS
    import pygame

    speak(text)


