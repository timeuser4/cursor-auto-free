from flask import Flask, jsonify
from data_manager import DatabaseManager
import sqlite3

app = Flask(__name__)
# 初始化DatabaseManager实例
database_manager = DatabaseManager()

@app.route('/get_account_info', methods=['GET'])
def get_account_info():
    # 调用DatabaseManager的pop方法获取账号信息
    account_info = database_manager.pop()
    
    if account_info:
        return jsonify(account_info)
    else:
        return jsonify({"error": "未找到账号信息"}), 404

if __name__ == '__main__':
    app.run(debug=True)
