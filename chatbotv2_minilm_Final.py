# Install the required libraries 

# !pip install --upgrade langchain openai  -q
# !pip install sentence_transformers -q
# !pip install unstructured -q
# !pip install unstructured[local-inference] -q
# !pip install jq
# !pip install flask

# importing the required libraries

import os
import getpass
from flask import Flask, request, jsonify, render_template
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
import pinecone
import requests
from langchain.embeddings import SentenceTransformerEmbeddings

import os
import getpass
import json
from pathlib import Path  
import requests
from flask import Flask, request, render_template, jsonify

from langchain.document_loaders import TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader

app = Flask(__name__)

# Set your API keys and environment variables here
os.environ["PINECONE_API_KEY"] = "YOUR_PINECONE_API_KEY"
os.environ["PINECONE_ENV"] = "YOUR_PINECONE_ENVIRONMENT"
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"



import os

# Define the path to the temporary directory
temp_directory = 'temp'

# Create the "temp" directory if it doesn't exist
if not os.path.exists(temp_directory):
    os.makedirs(temp_directory)
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            # Save the uploaded file to a temporary directory
            file_path = os.path.join('temp', file.filename)
            file.save(file_path)
            
            # Check the file extension and choose the loader accordingly
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.csv':
                loader = CSVLoader(file_path=file_path)
                documents = loader.load()
            elif file_extension == '.txt':
                loader = TextLoader(file_path)
                documents = loader.load()
            elif file_extension == '.html':
                loader = UnstructuredHTMLLoader(file_path)
                documents = loader.load()
            elif file_extension == '.json':
                documents = json.loads(Path(file_path).read_text())
            elif file_extension == '.md':
                loader = UnstructuredMarkdownLoader(file_path)
                documents = loader.load()
            elif file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
                documents = loader.load_and_split()

            # Load and split the documents
#             loader = TextLoader(file_path)
#             documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)

            # Initialize Pinecone and create an index
            index_name = "chatbotv2"
            #embeddings = OpenAIEmbeddings()
            
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            
            pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="YOUR_PINECONE_ENVIRONMENT")

            index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

            # Get the user's query
            query = request.form['query']

            # Perform similarity search
            similar_docs = index.similarity_search(query, k=1)
            content = similar_docs[0].page_content

            # Create a message list for OpenAI
            messages = [{"role": "user", "content": f"prompt: {query} context: {content}"}]

            # Define the OpenAI API parameters
            OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
            OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": 1.0,
                "top_p": 1.0,
                "n": 1,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 0,
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }

            # Send a POST request to OpenAI
            response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
            openai_response = response.json()
            generated_text = openai_response["choices"][0]["message"]["content"]

            return render_template('index.html', generated_text=generated_text)

    return render_template('index.html', generated_text=None)

if __name__ == '__main__':
    app.run(debug=True)
