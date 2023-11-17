import flask
from flask import jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if flask.request.method == 'POST':
        # 处理POST请求
        data = flask.request.json
        # 在这里对数据进行处理
        response = {"message": " Post, Hello, World!"}

        return jsonify(response)
    else:
        # 处理GET请求
        response = [{"message": "Get, Hello, World!"}]
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)