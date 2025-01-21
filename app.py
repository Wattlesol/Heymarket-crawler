from flask import Flask, jsonify, request
from threading import Thread
from dotenv import load_dotenv
from process_handler import async_process_list
from database_handler import Database
import os

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

        # thread = Thread(target=async_process_list, args=(data,))
        # thread.start()
        response = async_process_list(data)

        return jsonify({
            "message": response
        }), 200
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

        # Get column names for the result
        columns = [desc[0] for desc in db.cursor.description]
        data = dict(zip(columns, row))

        return jsonify({
            "data": data,
            "message": "Latest data fetched successfully."
        }), 200
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