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
            # Serialize lists and dictionaries to JSON strings
            delivered = json.dumps(data.get('delivered', []))  # Use 'delivered'
            failed = json.dumps(data.get('failed', []))
            responded = json.dumps(data.get('responded', []))
            opt_out = json.dumps(data.get('opt_out', []))
            reports = json.dumps(data.get('reports', {}))

            # SQL query to insert the data (exclude `created_at`)
            query = """
                INSERT INTO scraped_data (
                    list_name, msg_heading, content, campaign, send_to,
                    delivered, failed, responded, opt_out, reports
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data.get('list_name'),
                data.get('msg_heading'),
                data.get('content'),
                data.get('campaign'),
                data.get('send_to'),
                delivered,
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

    def fetch_all_data(self):
        """
        Fetches all data from the `scraped_data` table.
        """
        try:
            self.cursor.execute("SELECT * FROM scraped_data")
            rows = self.cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in self.cursor.description]

            # Convert rows into a list of dictionaries and deserialize JSON fields
            data = []
            for row in rows:
                record = dict(zip(columns, row))
                # Deserialize JSON strings to lists/dictionaries
                record['delivered'] = json.loads(record['delivered']) if record.get('delivered') else []  # Corrected field
                record['failed'] = json.loads(record['failed']) if record.get('failed') else []
                record['responded'] = json.loads(record['responded']) if record.get('responded') else []
                record['opt_out'] = json.loads(record['opt_out']) if record.get('opt_out') else []
                record['reports'] = json.loads(record['reports']) if record.get('reports') else {}
                data.append(record)

            return data
        except Exception as e:
            print("Error fetching data:", e)
            return []
        
    def fetch_data_by_campaign(self, campaign_name):
        """
        Fetches all data from the `scraped_data` table for a given campaign name.
        """
        try:
            query = "SELECT * FROM scraped_data WHERE campaign = %s"
            self.cursor.execute(query, (campaign_name,))
            rows = self.cursor.fetchall()

            # Get column names
            columns = [desc[0] for desc in self.cursor.description]

            # Convert rows into a list of dictionaries and deserialize JSON fields
            data = []
            for row in rows:
                record = dict(zip(columns, row))
                # Deserialize JSON strings to lists/dictionaries
                record['delivered'] = json.loads(record['delivered']) if record.get('delivered') else []
                record['failed'] = json.loads(record['failed']) if record.get('failed') else []
                record['responded'] = json.loads(record['responded']) if record.get('responded') else []
                record['opt_out'] = json.loads(record['opt_out']) if record.get('opt_out') else []
                record['reports'] = json.loads(record['reports']) if record.get('reports') else {}
                data.append(record)

            return data
        except Exception as e:
            print("Error fetching data by campaign:", e)
            return []