from flask import Flask, request, jsonify
from main import headline_generator
from main import paragraph_generator
from main import image_generator


app = Flask(__name__)

def get_article(prompt=""):
    tasks = [
        {
            'headline': headline_generator(prompt),
            'paragraph': paragraph_generator(),
            'image': image_generator(),
        },
    ]
    return tasks

@app.route('/api', methods=['GET'])
def get_article_without_input():
    return jsonify({'article': get_article()})

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
    app.run(debug=True)

