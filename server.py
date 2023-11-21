from flask import Flask, jsonify, request
import time

# 初始化Flask应用
app = Flask(__name__)

# 用于存储数据
data = {}
# 存储上一次的数据，用于和新数据对比
previous_data = {'id': 'previous_default'}

# 定义一个用于创建响应的函数，以减少代码重复
def create_response(new_data=False):

    response = {'new_data': new_data}
    if new_data:
        response.update({
            'sender': data.get('sender'),
            'subject': data.get('subject'),
            'content': data.get('content'),
            'id': data.get('id'),
            'sender_email_address': data.get('sender_email_address'),
            'thread_id': data.get('thread_id'),
        })
    return response

# 传文件
def create_file_response():
    response = {}
    response.update({
        'file_stream': data.get('file_stream'),
    })
    return response

@app.route('/getEmail', methods=['GET'])
def getEmail():
    """
    根据GET请求查询并返回数据，如果有新数据，立即返回；否则，等待一定时间。
    """
    timeout = int(request.args.get('timeout', 30))  # 设置超时时间，默认为30秒
    # 如果有新数据，立即返回
    if 'id' in data and data['id'] and previous_data['id'] != data['id']:
        previous_data['id'] = data['id']
        return jsonify(create_response(new_data=True))

    # 如果没有新数据，等待直到超时
    wait_time = 0
    while wait_time < timeout:
        if 'id' in data and data['id'] and previous_data['id'] != data['id']:
            previous_data['id'] = data['id']
            return jsonify(create_response(new_data=True))
        time.sleep(1)  # 休眠1秒，再次检查
        wait_time += 1

    # 超时后，没有新数据响应
    return jsonify(create_response())

@app.route('/postEmptyFile', methods=['POST'])
def post_empty_file():
    return jsonify(create_file_response())


@app.route('/postEmail', methods=['POST'])
def post_email():
    """
    接收POST请求，存储数据并返回。
    """
    global data
    data = request.get_json()
    return jsonify(create_response(new_data=True))


@app.route('/postFile', methods=['POST'])
def post_file():
    """
    接收POST请求，存储数据并返回。
    """
    global data
    data = request.get_json()
    return jsonify(create_file_response())

@app.route('/postAll', methods=['POST'])
def post_all():
    # 确保请求中有JSON数据
    if request.is_json:
        # 获取请求中的JSON数据
        req_data = request.get_json()
        # 直接返回请求中的JSON数据
        response = jsonify(req_data)
        response.status_code = 200
        return response
    else:
        # 若请求中没有JSON数据，则返回错误
        return jsonify({"error": "Request must be JSON"}), 400

# 主程序入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)