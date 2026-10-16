from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
DB_FILE = "scores.db"

# ==========【新增：我们自己定义API密钥】==========
MY_API_KEY = "abcd1234xyz"  # 你可以随便改成一串字符，就是你的密钥
# ===============================================

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==========【新增：写一个校验密钥的函数，所有接口共用】==========
def check_api_key():
    # 从请求头拿密钥，约定头部字段叫 Authorization
    client_key = request.headers.get("Authorization")
    if client_key != MY_API_KEY:
        return False
    return True
# ============================================================


# 接口1：GET 获取全部成绩记录
@app.route("/api/scores", methods=["GET"])
def get_all_scores():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, score FROM scores")
    rows = cur.fetchall()
    conn.close()
    res = [{"name": r[0], "score": r[1]} for r in rows]
    return jsonify({"code":0, "data":res})

# 接口2：POST 新增一条成绩
@app.route("/api/score", methods=["POST"])
def add_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")
    if not name or score is None:
        return jsonify({"code":1, "msg":"缺少name或者score"}),400
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO scores(name,score) VALUES (?,?)",(name,score))
    conn.commit()
    conn.close()
    return jsonify({"code":0, "msg":"添加成功","data":{"name":name,"score":score}})

# 接口3：GET 根据姓名查询单个成绩
@app.route("/api/score/<name>", methods=["GET"])
def get_one_score(name):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name,score FROM scores WHERE name=?",(name,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify({"code":0,"data":{"name":row[0],"score":row[1]}})
    else:
        return jsonify({"code":1,"msg":"没有找到该用户记录"}),404

if __name__ == "__main__":
    app.run(debug=True, port=5003)