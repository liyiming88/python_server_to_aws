import http.server
import socketserver

# 创建处理GET请求的处理器
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

# 定义服务器的地址
host = 'localhost'
port = 3000
address = (host, port)

# 创建服务器对象
server = socketserver.TCPServer(address, MyRequestHandler)

# 启动服务器
print(f'Starting server on http://{host}:{port}')
server.serve_forever()