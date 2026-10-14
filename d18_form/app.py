from flask import Flask, render_template,request    
import json
import os

app = Flask(__name__)
# POST表单必须配置密钥，本地练习随便写一串字符就行
app.secret_key = "my_secret_123"
JSON_FILE = "records.json"

# 初始化json文件，不存在就创建空列表
def init_json():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE,"w",encoding="utf-8") as f:
            json.dump([],f,ensure_ascii=False,indent=2)

# 读取全部历史记录
def read_records():
    init_json()
    with open(JSON_FILE,"r",encoding="utf-8") as f:
        return json.load(f)            
# 添加单条记录
def add_record(name, score):
    records = read_records()
    records.append({"name": name, "score": score})
    with open(JSON_FILE,"w",encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

@app.route('/', methods=["GET", "POST"])
def home():
    # ✅【固定默认用户，永远不会被表单POST覆盖！】
    default_name = "小雨"
    default_score = 95
    msg = ""


    if request.method == "POST":
        # 只拿表单提交的数据，专门用来新增记录
        submit_name = request.form.get("user_name","").strip()
        submit_score = request.form.get("user_score","").strip()
        if submit_name and submit_score:
            add_record(submit_name, submit_score)
            msg = "✅ 记录保存成功！已添加到历史列表"
        else:
            msg = "❌ 姓名和分数不能为空！"
    # 读取全部历史记录传给页面
    all_records = read_records()
    return render_template('home.html',
                           default_name=default_name,
                           default_score=default_score,
                           msg=msg,
                           records=all_records)

if __name__ == '__main__':
    app.run(debug=True, port=5002)