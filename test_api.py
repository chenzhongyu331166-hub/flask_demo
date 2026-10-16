import requests

base_url = "http://127.0.0.1:5003"
# =========【新增：请求头部，携带API Key】========
headers = {
    "Authorization": "abcd1234xyz"
}
# =============================================

print("====测试1 GET /api/scores 获取全部成绩====")
resp1 = requests.get(f"{base_url}/api/scores", headers=headers)
print(resp1.json())

print("\n====测试2 POST /api/score 添加成绩====")
resp2 = requests.post(f"{base_url}/api/score", json={"name":"张小丽","score":28}, headers=headers)
print(resp2.json())

print("\n====测试3 GET /api/score/张小丽 查询单人成绩====")
resp3 = requests.get(f"{base_url}/api/score/张小丽", headers=headers)
print(resp3.json())