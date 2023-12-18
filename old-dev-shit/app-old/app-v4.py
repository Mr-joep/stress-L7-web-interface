from flask import Flask, render_template, jsonify, request
import requests
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    # Read content from the "combined_output.txt" file
    file_content = read_file_content()

    return render_template('index.html', file_content=file_content)

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

@app.route('/file_content')
def get_file_content():
    # Read content from the "combined_output.txt" file
    file_content = read_file_content()
    return jsonify({'file_content': file_content})

@app.route('/save_request_website', methods=['POST'])
def save_website():
    # Get the website from the request
    website = request.form.get('website')

    # Save the website to a text file
    save_website_to_file(website)

    return 'Website saved successfully!'

def save_website_to_file(website):
    # Construct the path to the "websites.txt" file
    file_path = os.path.join("requests_combined", "websites.txt")

    # Save the website to the file
    with open(file_path, "a") as file:
        file.write(website + '\n')

def read_file_content():
    # Construct the path to the "combined_output.txt" file
    file_path = os.path.join("requests_combined", "combined_output.txt")

    # Read content from the "combined_output.txt" file
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = "File not found."

    return file_content

if __name__ == '__main__':
    app.run(debug=True)
