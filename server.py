import flask
from flask import jsonify, request

app = flask.Flask(__name__)

data = {}
previous_data = {'id':'previous_default'}

@app.route('/', methods=['GET'])
def hello():
    if 'id' in data and data['id']:
        if previous_data['id'] != data['id']:
            response = {
                'sender': data.get('sender'),
                'subject': data.get('subject'),
                'content': data.get('content'),
                'id': data.get('id'),
                'new_data': True
            }
            previous_data['id'] = data['id']
        else:
            response = {
            'new_data': False
        }
    else:
        response = {
            'new_data': False
        }
    return jsonify(response)

@app.route('/postdata', methods=['POST'])
def post_data():
    global data
    data = request.get_json()
    
    response = {
        'sender': data.get('sender'),
        'subject': data.get('subject'),
        'content': data.get('content'),
        'id': data.get('id')
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)