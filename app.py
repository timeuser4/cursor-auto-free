import time
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from data_manager import DatabaseManager

app = Flask(__name__)

# 设置 CORS，允许跨域
CORS(app)

# 设置 SocketIO 的 CORS 配置
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:8080", "http://127.0.0.1:8080"])

# 当客户端连接时，推送剩余账号数量
@socketio.on('connect', namespace='/')
def handle_connect():
    send_remaining_count(request.sid)

def send_remaining_count(towho=None):
    database_manager = DatabaseManager()
    remaining_size = database_manager.size()
    if towho:
        socketio.emit('remain_counts', {'remaining': remaining_size}, namespace='/', to=towho)
    else:
        socketio.emit('remain_counts', {'remaining': remaining_size})

def update_remaining_count():
    '''
    每秒钟推送一次剩余账号数量
    '''
    while True:
        time.sleep(1)
        send_remaining_count()

@app.route('/get_account_info', methods=['GET'])
def get_account_info():
    database_manager = DatabaseManager()
    account_info = database_manager.pop()
    if account_info:
        account_name = account_info.get('account')
        print(f'pop account: {account_name}, now remaining size: {database_manager.size()}')
        return jsonify(account_info)
    else:
        return jsonify({"error": "未找到账号信息"}), 404

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # 使用 socketio.run() 启动服务器，而不是直接使用 app.run()
    socketio.start_background_task(update_remaining_count)
    socketio.run(app, debug=True, port=8080)
