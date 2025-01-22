from flask import Flask, jsonify, request
from threading import Thread
from dotenv import load_dotenv
from process_handler import async_process_list
from database_handler import Database
import os ,json

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/process_list', methods=['POST'])
def api_process_list():
    """
    Endpoint to process a list asynchronously.
    """
    try:
        data = request.get_json()
        list_rec = data.get('list_rec')
        rec_time = data.get('rec_time')
        username = data.get("username")
        password = data.get("password")

        if not (list_rec and rec_time and username and password):
            return jsonify({
                'error': "Missing required fields. Provide 'list_rec', 'rec_time', 'username', and 'password'."
            }), 400

        thread = Thread(target=async_process_list, args=(data,))
        thread.start()

        return jsonify({
            "message": "Request submitted successfully. Scraping is in progress."
        }), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    """
    Endpoint to fetch all scraped data from the database.
    """
    try:
        db = Database()
        data = db.fetch_all_data()

        if not data:
            return jsonify({"message": "No data found."}), 404

        return jsonify({
            "data": data,
            "message": "Data fetched successfully."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_last_data', methods=['GET'])
def get_last_data():
    """
    Endpoint to fetch the most recent record from the database.
    """
    try:
        db = Database()
        query = "SELECT * FROM scraped_data ORDER BY created_at DESC LIMIT 1"
        db.cursor.execute(query)
        row = db.cursor.fetchone()

        if not row:
            return jsonify({"message": "No data found."}), 404

        # Get column names
        columns = [desc[0] for desc in db.cursor.description]
        record = dict(zip(columns, row))

        # Deserialize JSON fields
        record['delivered'] = json.loads(record['delivered']) if record.get('delivered') else []
        record['failed'] = json.loads(record['failed']) if record.get('failed') else []
        record['responded'] = json.loads(record['responded']) if record.get('responded') else []
        record['opt_out'] = json.loads(record['opt_out']) if record.get('opt_out') else []
        record['reports'] = json.loads(record['reports']) if record.get('reports') else {}

        return jsonify({
            "data": record,
            "message": "Latest data fetched successfully."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/get_campaign_data', methods=['POST'])
def get_campaign_data():
    """
    Endpoint to fetch all data for a specific campaign name.
    """
    # Parse JSON body
    data = request.get_json()
    campaign_name = data.get('campaign') if data else None

    if not campaign_name:
        return jsonify({"error": "Campaign name is required."}), 400

    try:
        db = Database()
        results = db.fetch_data_by_campaign(campaign_name)

        if not results:
            return jsonify({"message": f"No data found for campaign '{campaign_name}'."}), 404

        return jsonify({"data": results, "message": f"Data fetched successfully for campaign '{campaign_name}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def hello_world():
    """
    Health check endpoint.
    """
    return jsonify({"message": "API is running successfully!"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)