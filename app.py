import flask
from flask import request, jsonify
from ai import get_answer, load_index

app = flask.Flask(__name__)
app.config["DEBUG"] = True

index_file = "./indexes/20200627-193007_questions_answers"

answer = {'text': 'This is an answer', 'confidence': 0.8}
index = load_index(index_file)


@app.route('/', methods=['GET'])
def home():
    return "<p>Chatbot prototype</p>"


@app.route('/api/v1/answers', methods=['GET'])
def api_answers():
    if 'q' in request.args:
        question = request.args['q']
    else:
        return "Error: No question field provided. Please specify a question (q=...)."
    return jsonify(get_answer(index, question))


if __name__ == "__main__":
    app.run()
