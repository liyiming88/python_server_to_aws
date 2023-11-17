import flask
import logging
from flask import jsonify, request

app = flask.Flask(__name__)
app.config['DEBUG'] = True
logging.basicConfig(filename='app.log', level=logging.INFO)

@app.route('/', methods=['GET'])
def hello():
    response = [{"message": "Hello, World ma!"}]
    return jsonify(response)

@app.route('/postdata', methods=['POST'])
def post_data():
    data = request.get_json()
    sender = data.get('sender')
    subject = data.get('subject')
    content = data.get('content')
    id = data.get('id')
    
    # 在这里对接收到的数据进行处理，可以根据需求自定义逻辑
    
    response = {
        "sender": sender,
        "subject": subject,
        "content": content,
        "id": id
    }

    logger = logging.getLogger('postdata')
    logger.info("Received data:")
    logger.info("Sender: %s", sender)
    logger.info("Subject: %s", subject)
    logger.info("Content: %s", content)
    logger.info("ID: %s", id)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
