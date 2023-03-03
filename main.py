"""
import os
from dotenv import load_dotenv
load_dotenv()

from src.models import ModelInteraction, DocumentInteraction
from src.crawl_data import crawl_url

from flask import Flask,request
import json
from flask_cors import CORS

# print(os.environ["OPENAI_API_KEY"])
# print(os.getenv("REDIS_HOST"))

documentInteraction = DocumentInteraction()

app = Flask(__name__)
CORS(app)

@app.route("/")
async def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/wiki_retrieve/', methods=['POST'])
def listen_url():
    url = request.json['url']
    documentInteraction.insert_document(crawl_url(url))
    documentInteraction.processing_document()
    payload = documentInteraction.get_data()
    print(payload)
    # payload = [["AI is used to show intelligence in activities such as speech recognition, computer vision, and language translation"], ["Examples of AI applications include web search engines (Google Search), recommendation systems (YouTube, Amazon, Netflix), understanding human speech (Siri, Alexa), self-driving cars (Waymo), generative or creative tools (ChatGPT, AI art), automated decision-making and strategic game systems (chess, Go)"], ["AI is used in a wide range of topics and activities"]]
    response = {
        "payload" : json.dumps(payload)
    }
    return response
    

@app.route('/api/user_interact/', methods=['POST'])
def listen_user():
    sentence = request.json['sentence']
    prompt = request.json['prompt']
    if (prompt == "Explain more about this"):
        payload = documentInteraction.user_click_sentence_expand(sentence)

        print(payload)
        response = {
            "payload" : json.dumps(payload)
        }
        return response
    elif (prompt == "Show me the references"):
        payload = documentInteraction.user_click_sentence_get_ref(sentence)

        print(payload)
        response = {
            "payload" : json.dumps(payload)
        }
        return response
    
    return "Error"


if __name__ == '__main__':
    app.run(debug=True)


"""

from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
