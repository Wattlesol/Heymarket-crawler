import os
import json
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.getenv('DB_NAME')))
            self.cursor.execute("USE {}".format(os.getenv('DB_NAME')))
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    list_name VARCHAR(255),
                    timestamp VARCHAR(255),
                    content TEXT,
                    delivered TEXT,
                    failed TEXT,
                    responded TEXT,
                    opt_out TEXT,
                    campaign VARCHAR(255),
                    send_to VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Exception as e:
            print("Error initializing database:", e)

    def save_scraped_data(self, data):
        try:
            query = """
            INSERT INTO scraped_data (list_name, timestamp, content, delivered, failed, responded, opt_out, campaign, send_to)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                data['List'], data['timeStamp'], data['Content'],
                json.dumps(data['deliverd']), json.dumps(data['failed']),
                json.dumps(data['responded']), json.dumps(data['opt_out']),
                data['Campaign'], data['send_to']
            ))
            self.connection.commit()
        except Exception as e:
            print("Error while saving data to database:", e)
        finally:
            self.cursor.close()
            self.connection.close()
