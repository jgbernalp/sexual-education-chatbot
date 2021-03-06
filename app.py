import os
import flask
from flask import request, jsonify, render_template
from index import get_answer, load_index

app = flask.Flask(__name__)

index_file = "./indexes/runtime"

index = load_index(index_file)


@app.route('/', methods=['GET'])
def home():
    answers = []
    if 'q' in request.args:
        question = request.args['q']
        answers = get_answer(index, question)

    return render_template('home.html', answer=answers[0] if len(answers) > 0 else "", second_answer=answers[1] if len(answers) > 1 else "")


@app.route('/api/v1/answers', methods=['GET'])
def api_answers():
    if 'q' in request.args:
        question = request.args['q']
    else:
        return "Error: No question field provided. Please specify a question (q=...)."
    return jsonify(get_answer(index, question))


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
