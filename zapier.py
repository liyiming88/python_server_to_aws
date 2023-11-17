import flask
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    response = [{"message": "Hello, World!"}]
    return jsonify(response)

@app.route('/postdata', methods=['POST'])
def post_data():
    data = flask.request.json
    # 在这里对接收到的数据进行处理
    response = {"message": "Data received successfully"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)