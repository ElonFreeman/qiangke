import requests
from bs4 import BeautifulSoup
import time
# 定义选课页面的URL
url = 'http://example.com/course_selection'  # 替换为实际的选课页面URL
# 模拟登录页面（如果有的话）
login_url = 'http://example.com/login'  # 替换为实际的登录页面URL
login_data = {
'username': 'your_username',  # 替换为实际的用户名
'password': 'your_password'   # 替换为实际的密码
}
# 模拟填写并提交选课表单
def submit_course_selection():
  # 发送GET请求获取页面内容
 response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
# 找到选课表单并获取所有输入字段的名称和值
form = soup.find('form')
form_data = {}
for input_tag in form.find_all('input'):
 name = input_tag['name']
value = input_tag.get('value', '')
form_data[name] = value
# 填写选课表单（根据实际情况修改）
form_data['course_name'] = '计算机科学导论'  # 替换为你想选的课程名称
form_data['section'] = '01'  # 替换为合适的课程节数或班级代码
form_data['student_id'] = '123456789'  # 替换为你的学生ID号
form_data['submit'] = 'Submit'  # 提交按钮的文本或值，根据实际情况修改
# 发送POST请求提交选课表单
headers = {
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'  # 根据实际情况修改头部信息
}
response = requests.post(url, data=form_data, headers=headers)
print(response.text)  # 查看服务器响应的HTML内容（如果有的话）
if __name__ == '__main__':
 # 模拟登录（如果有的话）
 login_response = requests.post(login_url, data=login_data)
print(login_response.text)  # 查看登录页面的HTML内容（如果有的话）
# 等待一段时间让页面加载完成（可选）
time.sleep(5)  # 等待5秒，根据实际情况调整等待时间
# 提交选课表单
submit_course_selection()