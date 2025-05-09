# Cursor Pro 自动化工具使用说明
## 使用方法
```bash
conda create -n cursor_free python=3.10
conda activate cursor_free
pip install -r requirements.txt
```
## 启动
```bash
conda activate cursor_free
python app.py
```
打开index.html，点击获取账号信息即可

## TODO：
- [ ] client完成
- [ ] 随机信息查重
- [ ] 数据库升级sqlite3 -> mysql
- [ ] 定期清理screenshots文件夹（集成到_main线程中）
