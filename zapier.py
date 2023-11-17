import flask
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/')
def hello():
    response = {"message": "Hello, World!"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)