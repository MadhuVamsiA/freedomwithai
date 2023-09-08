import os
from flask import Flask, request, render_template, jsonify

import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
import json
from pathlib import Path
from langchain.embeddings import SentenceTransformerEmbeddings

app = Flask(__name__)

# Set your API key of serpapi
serpapi_key = "899493b418cb3b354dbd4ebbb9b8e2d1dfc505e1435e6b6fdca906fbe22096d7"

# Set your OpenAI API key
OPENAI_API_KEY = "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"

# Initialize Pinecone client
import pinecone
pinecone.init(api_key="0d42b314-e9e0-4fc0-add3-2b848c736c9d", environment="gcp-starter")

# Define the Pinecone index name
index_name = "chatbotv2"

# Function to extract data from a URL
def extract_data_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

           
            extracted_data = ""
            for paragraph in soup.find_all('p'):
                extracted_data += paragraph.text + "\n"

            return extracted_data
        else:
            return "Failed to retrieve data from the URL."
    except Exception as e:
        return str(e)

# Function to generate text using OpenAI
def generate_text(query, content):
    # Define your prompt and context
    prompt = query
    context = content

    # Create a message list with the user message (prompt) and context message
    messages = [
        {"role": "user", "content": f"prompt: {prompt} context: {context}"}
    ]

    # Define the payload with the modified messages field
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0,
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
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Parse and use the response from OpenAI
    openai_response = response.json()
    generated_text = openai_response["choices"][0]["message"]["content"]

    return generated_text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_search = request.form["input_search"]

        # Initialize the GoogleSearchResults object with your API key and query
        search = GoogleSearch({"q": input_search, "api_key": serpapi_key})

        # Perform the search and retrieve the results
        results = search.get_dict()

        # Access the search results
        link = None
        for result in results.get("organic_results", []):
            link = result.get("link")
            break

        if link:
            data = extract_data_from_url(link)
            
            # Define the path to the temporary directory
            temp_directory = 'data'

            # Create the "temp" directory if it doesn't exist
            if not os.path.exists(temp_directory):
                os.makedirs(temp_directory)

            # Define the file path and name within the folder
            file_name = "data.txt"  # Replace with the desired file name
            file_path = os.path.join(temp_directory, file_name)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
            #################    
            loader = TextLoader(file_path)
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            
            ############
            
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            
            index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
            
             # Get the user's query
            query = request.form['query']

            # Perform similarity search
            similar_docs = index.similarity_search(query, k=1)
            content = similar_docs[0].page_content

    
    
            generated_text = generate_text(query, content)
        else:
            generated_text = "No search results found."

        return render_template("index.html", generated_text=generated_text)
    
    return render_template("index.html", generated_text=None)

if __name__ == "__main__":
    app.run(debug=True)
