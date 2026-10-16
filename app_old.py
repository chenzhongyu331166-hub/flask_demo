from flask import Flask

# 创建web应用实例
app=Flask(__name__)

# 路由1：首页 /
@app.route('/')
def index():
   return "欢迎来到Flask作业网站！访问 /readme 查看README内容"

# 路由2：README内容 /
@app.route('/readme')
def readme():
    with open("README.md","r",encoding="utf-8") as f:
        content=f.read()
    return content

# 启动服务
if __name__=="__main__":
    app.run(debug=True,port=5001)  # debug=True表示调试模式，代码修改后会自动重启服务 
