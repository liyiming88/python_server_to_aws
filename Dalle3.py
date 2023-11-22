from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 你必须设置你自己的OpenAI密钥
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # 从POST请求的body中获取prompt
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "Missing 'prompt' field in request body"}), 400

    # 设置到OpenAI的请求参数
    openai_payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "style": "natural"
    }
    
    # 设置请求头，包括认证信息
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    # 向OpenAI发送POST请求
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        json=openai_payload,
        headers=headers
    )
    
    # 将OpenAI响应的内容返回给原始请求者
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=28256)