# Install the required libraries 

# !pip install -q openai 
# !pip install Flask
# !pip install requests


# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import requests
import json

# Create a Flask web application instance
app = Flask(__name__)

# Define your OpenAI API key and API URL
OPENAI_API_KEY = "Enter openai API key"
OPENAI_API_URL = "enter the openai API url"

# Define a route for the root URL '/'
@app.route('/')
def index():
    # Render an HTML template called 'index.html' when a user accesses the root URL
    return render_template('index.html')

# Define a route for '/get_response' that handles POST requests
@app.route('/get_response', methods=['POST'])
def get_response():
    # Get the user's input from the submitted form
    prompt = request.form['prompt']

    # Define the payload to send to the OpenAI API
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    # Define the headers for the HTTP request to the OpenAI API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Send a POST request to the OpenAI API with the payload and headers
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, stream=False)
    response_data = response.json()
    # Extract the content of the response from the API
    content = response_data['choices'][0]['message']['content']

    # Render an HTML template with the user's input and the AI's response
    return render_template('index.html', prompt=prompt, response=content)

# Run the Flask application if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)
