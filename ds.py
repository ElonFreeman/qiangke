import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class CourseSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("选课自动化工具")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # 创建样式
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        header = ttk.Label(main_frame, text="选课自动化工具", style='Header.TLabel')
        header.pack(pady=10)
        
        # 登录信息框架
        login_frame = ttk.LabelFrame(main_frame, text="登录信息", padding="10")
        login_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(login_frame, text="登录URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_url = ttk.Entry(login_frame, width=50)
        self.login_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(login_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(login_frame, width=50)
        self.username.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(login_frame, text="密码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(login_frame, width=50, show="*")
        self.password.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # 选课信息框架
        course_frame = ttk.LabelFrame(main_frame, text="选课信息", padding="10")
        course_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(course_frame, text="选课URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.course_url = ttk.Entry(course_frame, width=50)
        self.course_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="课程名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.course_name = ttk.Entry(course_frame, width=50)
        self.course_name.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="课程代码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.section = ttk.Entry(course_frame, width=50)
        self.section.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="学生ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.student_id = ttk.Entry(course_frame, width=50)
        self.student_id.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # 控制按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="开始选课", command=self.start_selection)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="清除日志", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 日志输出框架
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=15, font=('Consolas', 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # 设置默认值（用于演示）
        self.login_url.insert(0, "http://authserver.yznu.cn/authserver/login?service=https%3A%2F%2Fjwxt.yznu.edu.cn%2Fjsxsd%2F")
        self.course_url.insert(0, "https://jwxt.yznu.edu.cn/jsxsd/framework/xsMain.jsp")
        self.username.insert(0, "250223101156")
        self.password.insert(0, "zh12358")
        self.course_name.insert(0, "计算机科学导论")
        self.section.insert(0, "01")
        self.student_id.insert(0, "250223101156")
        
        # 配置网格权重
        login_frame.columnconfigure(1, weight=1)
        course_frame.columnconfigure(1, weight=1)
        
    def log_message(self, message):
        """添加消息到日志区域"""
        self.log_area.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_area.see(tk.END)
        
    def clear_log(self):
        """清除日志"""
        self.log_area.delete(1.0, tk.END)
        
    def start_selection(self):
        """开始选课过程"""
        # 禁用开始按钮，防止重复点击
        self.start_btn.config(state=tk.DISABLED)
        
        # 在新线程中运行选课过程
        thread = threading.Thread(target=self.run_selection)
        thread.daemon = True
        thread.start()
        
    def run_selection(self):
        """执行选课过程"""
        try:
            # 获取用户输入
            login_url = self.login_url.get()
            course_url = self.course_url.get()
            username = self.username.get()
            password = self.password.get()
            course_name_val = self.course_name.get()
            section_val = self.section.get()
            student_id_val = self.student_id.get()
            
            self.log_message("开始选课过程...")
            
            # 模拟登录
            self.log_message(f"尝试登录到: {login_url}")
            login_data = {
                'username': username,
                'password': password
            }
            
            # 创建会话对象
            session = requests.Session()
            
            # 发送登录请求
            login_response = session.post(login_url, data=login_data)
            self.log_message(f"登录响应状态: {login_response.status_code}")
            
            # 等待一段时间
            self.log_message("等待页面加载...")
            time.sleep(2)
            
            # 获取选课页面
            self.log_message(f"访问选课页面: {course_url}")
            response = session.get(course_url)
            self.log_message(f"选课页面响应状态: {response.status_code}")
            
            # 解析页面
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 找到选课表单
            form = soup.find('form')
            if not form:
                self.log_message("错误: 未找到选课表单")
                return
                
            form_data = {}
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                if name:
                    value = input_tag.get('value', '')
                    form_data[name] = value
            
            # 填写选课表单
            form_data['course_name'] = course_name_val
            form_data['section'] = section_val
            form_data['student_id'] = student_id_val
            form_data['submit'] = 'Submit'
            
            # 提交选课表单
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            self.log_message("提交选课表单...")
            response = session.post(course_url, data=form_data, headers=headers)
            self.log_message(f"表单提交响应状态: {response.status_code}")
            
            # 检查是否成功
            if response.status_code == 200:
                self.log_message("选课请求已提交！")
                # 这里可以添加更多的成功检查逻辑
            else:
                self.log_message("选课请求可能失败，请检查日志")
                
        except Exception as e:
            self.log_message(f"发生错误: {str(e)}")
        finally:
            # 重新启用开始按钮
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.log_message("选课过程完成")

def main():
    root = tk.Tk()
    app = CourseSelectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()