from io import BytesIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage, Image
import mysql.connector
class MyApp(App):
    def build(self):
        # Connect to the MySQL database (replace with your database connection details)
        db_config = {
                'host': 'localhost',
                'user': 'marj',
                'password': 'RAMIcpe211',
                'database': 'Ramibot',
            }

        try:
            con = mysql.connector.connect(**db_config)
            cursor = con.cursor()

                # Execute the SQL query
            sql = "SELECT img_url FROM program_img ORDER BY program_id ASC"
            cursor.execute(sql)

                # Create the main layout
            layout = BoxLayout(orientation='vertical')

                # Fetch and display images
            for row in cursor.fetchall():
                img_blob = row[0]
                image = self.create_image_from_blob(img_blob)
                layout.add_widget(image)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the database connection
            if 'con' in locals():
                cursor.close()
                con.close()

        return layout

    def create_image_from_blob(self, img_blob):
        try:
                # Convert the blob data to image
            img_data = BytesIO(img_blob)
            image = Image(texture=img_data.read(), allow_stretch=True)
            img_data.close()
            return image
        except Exception as e:
            print(f"Error creating image: {e}")
            return Image(source='shs.png')
                # Replace with a default image source

if __name__ == '__main__':
    MyApp().run()