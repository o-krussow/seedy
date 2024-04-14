from flask import Flask, request, jsonify
from main import get_paragraph, get_image_url
from nanoGPT import nanoGPT
import time

app = Flask(__name__)

def get_article(prompt=""):
    headline = gpt.generate()
    good_request = False
    while not good_request:
        try:
            print("Getting a paragraph and image")
            paragraph = get_paragraph(headline)
            image_url = get_image_url(headline)
            good_request = True
        except Exception as e:
            print(f"OpenAI Bad Request Error: {e}")
            print("Trying again...")

    tasks = [
        {
            'headline': headline,
            'image': image_url,
            'paragraph': paragraph,
        },
    ]
    return tasks

@app.route('/api', methods=['GET'])
def get_article_without_input():
    response = jsonify({'article': get_article()})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api', methods=['POST'])
def get_article_with_input():
    if request.is_json:
        prompt_json = request.get_json()

        #Post should come in format {prompt: <the prompt>}
        prompt = prompt_json["prompt"]
        
        #Pass prompt to get_article, which will pass prompt to headline generator
        return jsonify({'article': get_article(prompt)}), 201
    return {"error": "Request must be JSON"}, 415

if __name__ == '__main__':
    
    gpt = nanoGPT()

    #while True:
    #    time.sleep(10)

    app.run(debug=False)

