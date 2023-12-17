from flask import Flask, render_template, jsonify
import requests
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_status')
def check_status():
    try:
        response = requests.get('http://192.168.154.139/')
        if response.status_code >= 200 and response.status_code < 350:
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

if __name__ == '__main__':
    app.run(debug=True)
