from flask import Flask, jsonify, request
import time
import json

# 初始化Flask应用
app = Flask(__name__)

# 用于存储数据
data = {}
event_data = {}
email_data = {}
isEmailPosted = False

# 用于存储附件编码
attachment = {}
previous_attachment = {}
# 存储上一次的数据，用于和新数据对比
previous_data = {'id': 'previous_default'}

# 定义一个用于创建响应的函数，以减少代码重复
def create_email_response():
    global isEmailPosted
    response = {}
    response.update({
        'sender': email_data.get('sender'),
        'subject': email_data.get('subject'),
        'content': email_data.get('content'),
        'sender_email_address': email_data.get('sender_email_address'),
        'thread_id': email_data.get('thread_id'),
        'email_found': email_data.get('email_found')
    })
    isEmailPosted = True
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
    timeout = int(request.args.get('timeout', 10))  # 设置超时时间，默认为30秒
    if event_data is not None:
        return event_data
    else:
        wait_time = 0
        while wait_time < timeout:
            if event_data is not None:
                return event_data
            time.sleep(1)  # 休眠1秒，再次检查
            wait_time += 1

    # 超时后，没有新数据响应
    return jsonify({'event_found':False})

# 查找一次是否有新邮件
@app.route('/getEmail', methods=['GET'])
def getEmail():
    timeout = int(request.args.get('timeout', 10))  # 设置超时时间，默认为30秒
    if 'email_found' in email_data and email_data['email_found'] is not None and isEmailPosted:
        isEmailPosted = False
        return jsonify(create_email_response())
    else:
        # 如果没有新数据，等待直到超时
        wait_time = 0
        while wait_time < timeout:
            if 'email_found' in email_data and email_data['email_found'] is not None:
                isEmailPosted = False
                return jsonify(create_email_response())
            time.sleep(1)  # 休眠1秒，再次检查
            wait_time += 1
    isEmailPosted = False
    # 超时后，没有新数据响应
    return jsonify({'email_found':False})

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
        return jsonify(create_email_response())

    # 如果没有新数据，等待直到超时
    wait_time = 0
    while wait_time < timeout:
        if 'id' in data and data['id'] and previous_data['id'] != data['id']:
            previous_data['id'] = data['id']
            return jsonify(create_email_response(new_data=True))
        time.sleep(1)  # 休眠1秒，再次检查
        wait_time += 1

    # 超时后，没有新数据响应
    return jsonify(create_email_response())

# @app.route('/getAttachment', methods=['GET'])
# def get_attachment():
#     """
#     长轮询，如果attachment值更新，则返回它的值，之后再进入到长轮询中。
#     """
#     global attachment
#     global previous_attachment
#     timeout = int(request.args.get('timeout', 30))  # 设置超时时间，默认为30秒
#     wait_time = 0
#     while wait_time < timeout:
#         if attachment != previous_attachment and attachment:
#             previous_attachment = attachment
#             return jsonify({'file_stream': attachment, 'new_data':True})
#         time.sleep(1)  # 休眠1秒，再次检查
#         wait_time += 1
#     return jsonify({'new_data':False})

@app.route('/getAttachment', methods=['GET'])
def get_attachment():
    global attachment
    return jsonify({'file_stream':attachment})

@app.route('/postEmptyFile', methods=['POST'])
def post_empty_file():
    return jsonify(create_file_response())


@app.route('/postEmail', methods=['POST'])
def post_email():
    """
    接收POST请求，存储数据并返回。
    """
    global email_data
    email_data = request.get_json()
    return jsonify(create_email_response())

@app.route('/postEvent', methods=['POST'])
def post_event():
    global event_data
    event_data = {}
    event_data = request.get_json()
    return event_data

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
    global data
    # 确保请求中有JSON数据
    if request.is_json:
        # 获取请求中的JSON数据
        req_data = request.get_json()
        # 直接返回请求中的JSON数据
        response = jsonify(req_data)
        response.status_code = 200
        data = response
        return response
    else:
        # 若请求中没有JSON数据，则返回错误
        return jsonify({"error": "Request must be JSON"}), 400
    


# 主程序入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)