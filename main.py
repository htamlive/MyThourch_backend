import os
from dotenv import load_dotenv
load_dotenv()

from src.models import ModelInteraction, DocumentInteraction
from src.crawl_data import crawl_url

from flask import Flask,request
import json
from flask_cors import CORS
import openai
from flask_socketio import SocketIO, emit


# print(os.environ["OPENAI_API_KEY"])
# print(os.getenv("REDIS_HOST"))


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@socketio.on('process_stage')
def send_stage(stage):
    emit('stage_update', stage, broadcast=True)

documentInteraction = DocumentInteraction(send_stage)

@app.route("/")
async def hello_world():
    print(request)
    return "<p>Hello, World!</p>"

@app.route('/api/wiki_retrieve/', methods=['POST'])
def listen_url():
    print(request[:10] + '... ')
    url = request.json['url']
    openai.api_key = request.json['apiKey']

    send_stage("Crawling data from " + url)

    documentInteraction.insert_document(crawl_url(url))
    documentInteraction.processing_document()
    payload = documentInteraction.get_data()

    send_stage("Crawling data from " + url + " Done")
    print(payload[:10] + '... ')
    # payload = [["AI is used to show intelligence in activities such as speech recognition, computer vision, and language translation"], ["Examples of AI applications include web search engines (Google Search), recommendation systems (YouTube, Amazon, Netflix), understanding human speech (Siri, Alexa), self-driving cars (Waymo), generative or creative tools (ChatGPT, AI art), automated decision-making and strategic game systems (chess, Go)"], ["AI is used in a wide range of topics and activities"]]
    response = {
        "payload" : json.dumps(payload)
    }
    return response



    

@app.route('/api/user_interact/', methods=['POST'])
def listen_user():
    print(request)
    sentence = request.json['sentence']
    prompt = request.json['prompt']
    if (prompt == "Explain more about this"):
        payload, topics = documentInteraction.user_click_sentence_expand(sentence)

        print(payload[:10] + '... ')
        response = {
            "payload" : json.dumps(payload),
            "topics" : json.dumps(topics)
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
    socketio.run(app)