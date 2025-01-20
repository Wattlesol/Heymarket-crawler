# app.py
from flask import Flask, jsonify, request
from threading import Thread
from dotenv import load_dotenv
from process_handler import async_process_list

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/process_list', methods=['POST'])
def api_process_list():
    data = request.get_json()
    list_rec = data.get('list_rec', 'Test List')
    rec_time = data.get('rec_time', '2024 at 11:21 PM')
    username = data.get("username", '')
    password = data.get("password", "")
    if not {username and password}:
        return jsonify({'error': "Provide valid username and password"})

    # Start processing in a separate thread
    thread = Thread(target=async_process_list, args=(data,))
    thread.start()

    return jsonify({"message": "Request submitted successfully. Scraping is in progress."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)