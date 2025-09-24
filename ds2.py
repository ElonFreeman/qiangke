import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import random

class CourseSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("选课自动化工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 创建样式
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        style.configure('TButton', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        header = ttk.Label(main_frame, text="     选课自动化工具\nBY:elon_freeman&deepseek", style='Header.TLabel')
        header.pack(pady=10)
        
        # 登录信息框架
        login_frame = ttk.LabelFrame(main_frame, text="登录信息", padding="10")
        login_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(login_frame, text="登录URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_url = ttk.Entry(login_frame, width=60)
        self.login_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(login_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(login_frame, width=60)
        self.username.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(login_frame, text="密码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(login_frame, width=60, show="*")
        self.password.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # 选课信息框架
        course_frame = ttk.LabelFrame(main_frame, text="选课信息", padding="10")
        course_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(course_frame, text="选课URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.course_url = ttk.Entry(course_frame, width=60)
        self.course_url.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="课程名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.course_name = ttk.Entry(course_frame, width=60)
        self.course_name.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="课程代码:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.section = ttk.Entry(course_frame, width=60)
        self.section.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(course_frame, text="学生ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.student_id = ttk.Entry(course_frame, width=60)
        self.student_id.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # 设置框架
        settings_frame = ttk.LabelFrame(main_frame, text="高级设置", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="最大重试次数:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.max_retries = ttk.Entry(settings_frame, width=10)
        self.max_retries.insert(0, "3")
        self.max_retries.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(settings_frame, text="超时时间(秒):").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.timeout = ttk.Entry(settings_frame, width=10)
        self.timeout.insert(0, "10")
        self.timeout.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # 控制按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        self.start_btn = ttk.Button(button_frame, text="开始选课", command=self.start_selection)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="停止", command=self.stop_selection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="清除日志", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # 日志输出框架
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=18, font=('Consolas', 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # 设置默认值
        self.login_url.insert(0, "http://authserver.yznu.cn/authserver/login?service=https%3A%2F%2Fjwxt.yznu.edu.cn%2Fjsxsd%2F")
        self.course_url.insert(0, "https://jwxt.yznu.edu.cn/jsxsd/framework/xsMain.jsp")
        self.username.insert(0, "250223101156")
        self.password.insert(0, "zh112358")
        self.course_name.insert(0, "计算机科学导论")
        self.section.insert(0, "01")
        self.student_id.insert(0, "250223101156")
        
        # 配置网格权重
        login_frame.columnconfigure(1, weight=1)
        course_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(1, weight=0)
        settings_frame.columnconfigure(3, weight=0)
        
        # 线程控制变量
        self.stop_requested = False
        
    def log_message(self, message):
        """添加消息到日志区域"""
        self.log_area.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_area.see(tk.END)
        self.status_var.set(message)
        
    def clear_log(self):
        """清除日志"""
        self.log_area.delete(1.0, tk.END)
        self.status_var.set("日志已清除")
        
    def stop_selection(self):
        """停止选课过程"""
        self.stop_requested = True
        self.log_message("用户请求停止选课...")
        
    def start_selection(self):
        """开始选课过程"""
        self.stop_requested = False
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
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
            
            # 获取设置
            try:
                max_retries = int(self.max_retries.get())
            except ValueError:
                max_retries = 3
                
            try:
                timeout_val = int(self.timeout.get())
            except ValueError:
                timeout_val = 10
            
            self.log_message("开始选课过程...")
            self.log_message(f"配置: 最大重试次数={max_retries}, 超时时间={timeout_val}秒")
            
            if self.stop_requested:
                self.log_message("选课已取消")
                return
            
            # 创建会话对象
            session = requests.Session()
            
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # 登录过程 - 带重试机制
            login_success = False
            for attempt in range(max_retries):
                if self.stop_requested:
                    self.log_message("选课已取消")
                    return
                    
                try:
                    self.log_message(f"尝试登录 ({attempt + 1}/{max_retries})...")
                    
                    login_data = {
                        'username': username,
                        'password': password
                    }
                    
                    login_response = session.post(login_url, data=login_data, headers=headers, timeout=timeout_val)
                    self.log_message(f"登录响应状态: {login_response.status_code}")
                    
                    # 检查登录是否成功（这里需要根据实际网站调整判断逻辑）
                    if login_response.status_code == 200:
                        login_success = True
                        self.log_message("✓ 登录成功！")
                        break
                    else:
                        self.log_message("登录可能失败，检查用户名密码")
                        
                except requests.exceptions.RequestException as e:
                    wait_time = random.uniform(2, 5)
                    self.log_message(f"登录请求失败: {e}，等待{wait_time:.2f}秒后重试...")
                    time.sleep(wait_time)
            
            if not login_success:
                self.log_message("✗ 登录多次失败，终止选课过程")
                return
            
            if self.stop_requested:
                self.log_message("选课已取消")
                return
            
            # 等待随机时间
            wait_time = random.uniform(1, 3)
            self.log_message(f"等待页面加载 ({wait_time:.2f}秒)...")
            time.sleep(wait_time)
            
            # 获取选课页面 - 带重试机制
            page_response = None
            for attempt in range(max_retries):
                if self.stop_requested:
                    self.log_message("选课已取消")
                    return
                    
                try:
                    self.log_message(f"获取选课页面 ({attempt + 1}/{max_retries})...")
                    page_response = session.get(course_url, headers=headers, timeout=timeout_val)
                    self.log_message(f"页面响应状态: {page_response.status_code}")
                    break
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        wait_time = random.uniform(2, 5)
                        self.log_message(f"获取页面失败: {e}，等待{wait_time:.2f}秒后重试...")
                        time.sleep(wait_time)
                    else:
                        self.log_message("✗ 获取页面多次失败")
                        return
            
            if self.stop_requested:
                self.log_message("选课已取消")
                return
            
            # 解析页面
            soup = BeautifulSoup(page_response.content, 'html.parser')
            
            # 找到选课表单
            form = soup.find('form')
            if not form:
                self.log_message("✗ 错误: 未找到选课表单")
                return
                
            # 提取表单数据
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
            
            # 提交选课表单 - 带重试机制
            submit_headers = headers.copy()
            submit_headers.update({
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': course_url
            })
            
            submit_success = False
            for attempt in range(max_retries):
                if self.stop_requested:
                    self.log_message("选课已取消")
                    return
                    
                try:
                    self.log_message(f"提交选课表单 ({attempt + 1}/{max_retries})...")
                    response = session.post(course_url, data=form_data, headers=submit_headers, timeout=timeout_val + 5)
                    self.log_message(f"提交响应状态: {response.status_code}")
                    
                    if response.status_code == 200:
                        submit_success = True
                        self.log_message("✓ 选课请求已提交！")
                        # 可以在这里添加结果解析逻辑
                        break
                    else:
                        self.log_message("提交可能失败")
                        
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        wait_time = random.uniform(3, 8)
                        self.log_message(f"提交失败: {e}，等待{wait_time:.2f}秒后重试...")
                        time.sleep(wait_time)
                    else:
                        self.log_message("✗ 提交多次失败")
            
            if submit_success:
                self.log_message("🎉 选课流程完成！请登录系统确认选课结果。")
            else:
                self.log_message("❌ 选课流程未完成，请检查网络连接或系统状态。")
                
        except Exception as e:
            self.log_message(f"💥 发生未预期的错误: {str(e)}")
        finally:
            # 重新启用开始按钮
            self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))
            self.log_message("选课过程结束")

def main():
    root = tk.Tk()
    app = CourseSelectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()