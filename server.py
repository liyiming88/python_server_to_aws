from flask import Flask, jsonify, request
import time

# 初始化Flask应用
app = Flask(__name__)

# 用于存储数据
data = {}

# 用于存储附件编码
attachment = {}
previous_attachment = {}
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

def create_event_response():

    response = {}
    response.update({
        'summary': data.get('summary'),
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time'),
        'attendee_emails': data.get('attendee_emails'),
        'event_found': data.get('event_found')
    })
    return response

# 传文件
def create_file_response():
    response = {}
    response.update({
        'file_stream': data.get('file_stream'),
    })
    return response

# 测试接口健康状态
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

# 查找一次是否有新event
@app.route('/getEvent', methods=['GET'])
def getEvent():
    return jsonify(create_event_response())

# 查找一次是否有新邮件
@app.route('/getEmail', methods=['GET'])
def getEmail():
    # 如果有新数据，立即返回
    if 'id' in data and data['id'] and previous_data['id'] != data['id']:
        previous_data['id'] = data['id']
        return jsonify(create_response(new_data=True))
    else:
        return jsonify({'new_data':False})

# 轮询是否有新邮件
@app.route('/getEmailPolling', methods=['GET'])
def getEmailPolling():
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

@app.route('/getAttachment', methods=['GET'])
def get_attachment():
    """
    长轮询，如果attachment值更新，则返回它的值，之后再进入到长轮询中。
    """
    global attachment
    global previous_attachment
    timeout = int(request.args.get('timeout', 30))  # 设置超时时间，默认为30秒
    wait_time = 0
    while wait_time < timeout:
        if attachment != previous_attachment and attachment:
            previous_attachment = attachment
            return jsonify({'file_stream': attachment, 'new_data':True})
        time.sleep(1)  # 休眠1秒，再次检查
        wait_time += 1
    return jsonify({'new_data':False})

@app.route('/postEmptyFile', methods=['POST'])
def post_empty_file():
    return jsonify(create_file_response())


@app.route('/postEmail', methods=['POST'])
def post_event():
    """
    接收POST请求，存储数据并返回。
    """
    global data
    data = request.get_json()
    return jsonify(create_response(new_data=True))

@app.route('/postEvent', methods=['POST'])
def post_email():
    """
    接收POST请求，存储数据并返回。
    """
    global data
    data = request.get_json()
    return jsonify(create_event_response())

# 从Zapier中上传文件数据至服务端
@app.route('/postFile', methods=['POST'])
def post_file():
    """
    接收POST请求，存储数据并返回上传成功。
    """
    global data
    global attachment
    data = request.get_json()
    attachment = data.get('file_stream')  # 保存data中file_stream的值到服务器变量中
    return jsonify(data)

# 接收Zapier传来的所有body键值对
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