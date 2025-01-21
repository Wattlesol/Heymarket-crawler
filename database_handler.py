import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor()

    def initialize_db(self):
        """
        Creates the `scraped_data` table if it does not already exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                list_name VARCHAR(255),
                msg_heading VARCHAR(255),
                content TEXT,
                campaign VARCHAR(255),
                send_to VARCHAR(255),
                deliverd TEXT,
                failed TEXT,
                responded TEXT,
                opt_out TEXT,
                reports TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()
        print("Database initialized successfully!")

    def save_scraped_data(self, data):
        """
        Saves the scraped data into the `scraped_data` table.
        """
        try:
            # Convert lists and dictionaries to JSON strings
            deliverd = json.dumps(data.get('deliverd', []))
            failed = json.dumps(data.get('failed', []))
            responded = json.dumps(data.get('responded', []))
            opt_out = json.dumps(data.get('opt_out', []))
            reports = json.dumps(data.get('reports', {}))

            # SQL query to insert the data
            query = """
                INSERT INTO scraped_data (
                    list_name, msg_heading, content, campaign, send_to,
                    deliverd, failed, responded, opt_out, reports
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data.get('List'),
                data.get('Msg_heading'),
                data.get('Content'),
                data.get('Campaign'),
                data.get('send_to'),
                deliverd,
                failed,
                responded,
                opt_out,
                reports
            )

            # Execute and commit the query
            self.cursor.execute(query, values)
            self.connection.commit()

            print("Data saved successfully!")
        except Exception as e:
            print("Error saving data to the database:", e)
        finally:
            self.cursor.close()
            self.connection.close()

    def fetch_all_data(self):
        """
        Fetches all data from the `scraped_data` table.
        """
        try:
            self.cursor.execute("SELECT * FROM scraped_data")
            rows = self.cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in self.cursor.description]

            # Convert rows to a list of dictionaries
            data = [dict(zip(columns, row)) for row in rows]
            return data
        except Exception as e:
            print("Error fetching data:", e)
            return []
        finally:
            self.cursor.close()
            self.connection.close()
