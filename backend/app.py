from models import ModelInteraction, DocumentInteraction
from crawl_data import crawl_url

from flask import Flask,request
import os
import json
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv('./key.env.local')

test = DocumentInteraction()

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/predict', methods=['POST'])
def predict():
    query = request.json.get("query")
    query_with_contexts = retrieve_from_gpt(query)
    print(query_with_contexts)
    bot = complete(query_with_contexts)

    return {"bot": bot}
    
if __name__ == '__main__':
    app.run(debug=True)


