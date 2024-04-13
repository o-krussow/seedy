from flask import Flask, request, jsonify
from main import get_headline
from main import get_paragraph
from main import get_image


app = Flask(__name__)

def get_article(prompt=""):
    headline = get_headline(prompt)
    paragraph = get_paragraph(headline)
    image = get_image()
    tasks = [
        {
            'headline': headline,
            'paragraph': paragraph,
            'image': image,
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

