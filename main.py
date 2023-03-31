#%%
import os
from dotenv import load_dotenv
load_dotenv()
REDIS_ACTIVATE = os.getenv("REDIS_ACTIVATE")
print(REDIS_ACTIVATE)

from src.models import ModelInteraction, DocumentInteraction
from src.crawl_data import crawl_url
from src.StageSender import StageSender

from flask import Flask,request
import requests
import json
from flask_cors import CORS
import openai
from flask_socketio import SocketIO, emit

#%%
# print(os.environ["OPENAI_API_KEY"])
# print(os.getenv("REDIS_HOST"))

def get_title_from_url(url):
    response = requests.get(url)
    # Extract the page title from the HTML content using string manipulation
    title_start = response.text.find("<title>") + len("<title>")
    title_end = response.text.find(" - Wikipedia</title>")
    title = response.text[title_start:title_end]

    # Print the page title
    return title

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


def def_send_stage(stage):
    print(stage)

stageSender = StageSender(socketio)
documentInteraction = DocumentInteraction(stageSender)

@app.route("/")
def hello_world():
    #print(request)
    return "<p>Hello, World!</p>"

@app.route('/api/wiki_retrieve/', methods=['POST'])
def listen_url():
    print(request)
    url = request.json['url']
    title = get_title_from_url(url)
    openai.api_key = request.json['apiKey']

    stageSender.send_stage("Crawling data from " + url)

    payload, topics = documentInteraction.insert_and_process_document(crawl_url(url))

    stageSender.send_stage("Crawling data from " + url + " Done")
    print(payload)
    # payload = [["AI is used to show intelligence in activities such as speech recognition, computer vision, and language translation"], ["Examples of AI applications include web search engines (Google Search), recommendation systems (YouTube, Amazon, Netflix), understanding human speech (Siri, Alexa), self-driving cars (Waymo), generative or creative tools (ChatGPT, AI art), automated decision-making and strategic game systems (chess, Go)"], ["AI is used in a wide range of topics and activities"]]
    response = {
        "payload" : json.dumps(payload),
        "topics" : json.dumps(topics),
        "title": json.dumps(title)
    }
    return response

@app.route('/api/test_wiki_retrieve/', methods=['POST'])
def test_listen_url():
    print(request)
    url = request.json['url']
    title = get_title_from_url(url)
    openai.api_key = request.json['apiKey']

    stageSender.send_stage("Crawling data from " + url)

    #payload, topics = documentInteraction.insert_and_process_document(crawl_url(url))

    stageSender.send_stage("Crawling data from " + url + " Done")

    #print(payload)
    # payload = [["AI is used to show intelligence in activities such as speech recognition, computer vision, and language translation"], ["Examples of AI applications include web search engines (Google Search), recommendation systems (YouTube, Amazon, Netflix), understanding human speech (Siri, Alexa), self-driving cars (Waymo), generative or creative tools (ChatGPT, AI art), automated decision-making and strategic game systems (chess, Go)"], ["AI is used in a wide range of topics and activities"]]
    
    #open json file
    with open(r'test\wiki_test.json') as json_file:
        response = json.load(json_file)
    
    
    return response


@app.route('/api/topic_retrieve_from_context/', methods=['POST'])
def listen_topics():
    context = request.json['context']
    payload = documentInteraction.extract_topic_from_database(context)

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

@app.route('/api/test_user_interact/', methods=['POST'])
def test_listen_user():
    print(request)
    prompt = request.json['prompt']
    if (prompt == "Explain more about this"):
        #open json file
        with open('test/user_interact_explain_test.json') as json_file:
            response = json.load(json_file)
        return response
    elif (prompt == "Show me the references"):
        #open json file
        with open('test/user_interact_ref_test.json') as json_file:
            response = json.load(json_file)
        return response
    
    return "Error"

#%%
#documentInteraction.insert_and_process_default_document()
#%%
if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
    # send_stage("Hello")

    # url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    # title = get_title_from_url(url)
    # openai.api_key = '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'

    # stageSender.send_stage("Crawling data from " + url)

    # payload, topics = documentInteraction.insert_and_process_document(crawl_url(url))

    # stageSender.send_stage("Crawling data from " + url + " Done")
    # # print(payload)
    # # payload = [["AI is used to show intelligence in activities such as speech recognition, computer vision, and language translation"], ["Examples of AI applications include web search engines (Google Search), recommendation systems (YouTube, Amazon, Netflix), understanding human speech (Siri, Alexa), self-driving cars (Waymo), generative or creative tools (ChatGPT, AI art), automated decision-making and strategic game systems (chess, Go)"], ["AI is used in a wide range of topics and activities"]]
    # response = {
    #     "payload" : json.dumps(payload),
    #     "topics" : json.dumps(topics),
    #     "title": json.dumps(title)
    # }

    # print(response)

    # # save response to test file
    # with open(r'test\wiki_test_2.json', 'w') as outfile:
    #     json.dump(response, outfile)

    # test_sentences = payload[0][0]
    # payload, topics = documentInteraction.user_click_sentence_expand(test_sentences)

    # response = {
    #         "payload" : json.dumps(payload),
    #         "topics" : json.dumps(topics)
    # }

    # print(response)

    # # save response to test file
    # with open(r'test\wiki_test_3.json', 'w') as outfile:
    #     json.dump(response, outfile)

    # payload = documentInteraction.user_click_sentence_get_ref(test_sentences)

    # print(payload)
    # response = {
    #     "payload" : json.dumps(payload)
    # }
    # print(response)

    # # save response to test file
    # with open(r'test\wiki_test_4.json', 'w') as outfile:
    #     json.dump(response, outfile)
    
# %%
# %%
