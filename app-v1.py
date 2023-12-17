from flask import Flask, render_template, jsonify
import requests
from flask_cors import CORS
import subprocess
import time

app = Flask(__name__)
CORS(app)

requests_counter = 0
requests_last_update = time.time()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_status')
def check_status():
    try:
        response = requests.get('http://192.168.154.139/')
        if response.status_code >= 200 and response.status_code < 350:
            update_requests_counter()
            return jsonify({'status': 'online', 'statusCode': response.status_code})
        else:
            return jsonify({'status': 'offline', 'statusCode': response.status_code})
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/run_load_script', methods=['POST'])
def run_load_script():
    try:
        # Run the load.py script using subprocess
        subprocess.run(['python', 'load.py'])
        return 'Script executed successfully!'
    except Exception as e:
        return f'Error executing script: {str(e)}'

@app.route('/get_requests_per_second')
def get_requests_per_second():
    update_requests_counter()
    return jsonify({'requests_per_second': calculate_requests_per_second()})

def update_requests_counter():
    global requests_counter, requests_last_update
    current_time = time.time()
    if current_time - requests_last_update >= 1:
        requests_counter = 1
        requests_last_update = current_time
    else:
        requests_counter += 1

def calculate_requests_per_second():
    return requests_counter

if __name__ == '__main__':
    app.run(debug=True)
