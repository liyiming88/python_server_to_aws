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
    """
    根据数据创建响应内容。

    参数:
    new_data - 布尔值，指示是否有新数据。

    返回:
    包含响应数据的字典。
    """
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

@app.route('/', methods=['GET'])
def hello():
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

@app.route('/postdata', methods=['POST'])
def post_data():
    """
    接收POST请求，存储数据并返回。
    """
    global data
    data = request.get_json()
    return jsonify(create_response(new_data=True))

# 主程序入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)