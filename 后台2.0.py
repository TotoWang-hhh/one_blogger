import requests
import tkinter as tk
import time
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk
import markdown
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
import webbrowser

# 读取文件
def open_file(file_path):
    with open(file_path, 'wb+') as f:
        return f.read()

def writeToken():
    token=token_enter.get()
    user=user_enter.get()
    email=email_enter.get()
    with open("./settings/token.set",'w') as f:
        f.write(token)
    with open("./settings/user.set",'w') as f:
        f.write(user)
    with open("./settings/email.set",'w') as f:
        f.write(email)
    token_win.destroy()

#读取设置
with open("./settings/token.set",'r') as f:
    token=f.read()
with open("./settings/user.set",'r') as f:
    user=f.read()
with open("./settings/email.set",'r') as f:
    email=f.read()
with open("./settings/post_formwork.set",'r') as f:
    post_formwork=f.read()


def post(content,name):
    global user
    upload_file(content,name+".html",user,user+".github.io","post/")

def md_post(content,name,title,linkedRepo):
    html_cont=markdown.Markdown(content)
    html=post_formwork.format(title=title,name=name,content=content,linked_repo=linkedRepo)
    post(html,name)

# 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    return data_b64


# 上传文件
def upload_file(file_data,file_name,user,repo,path=""):
    global token,email
    url = "https://api.github.com/repos/"+user+"/"+repo+"/contents/"+path+file_name  # 用户名、库名、路径
    headers = {"Authorization": "token " + token}
    content = file_base64(file_data)
    data = {
        "message": "message",
        "committer": {
            "name": user,
            "email": email
        },
        "content": file_data
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    print(re_data)
    print(re_data['content']['sha'])
    print("https://cdn.jsdelivr.net/gh/[user]/[repo]/[path]"+file_name)

def md():
    md_win=tk.Tk()
    md_win.title('MarkDown编辑器')
    tk.Label(md_win,text='博客名称').pack()
    name_enter=ttk.Entry(md_win)
    name_enter.pack(fill=tk.X)
    tk.Label(md_win,text='博客标题').pack()
    title_enter=ttk.Entry(md_win)
    title_enter.pack(fill=tk.X)
    tk.Label(md_win,text='链接的存储库（可选）').pack()
    linkedRepo_enter=ttk.Entry(md_win)
    linkedRepo_enter.pack(fill=tk.X)
    tk.Label(md_win,text='博客内容').pack()
    scroll = tk.Scrollbar(md_win)
    md_enter=tk.Text(md_win)
    # 将滚动条填充
    scroll.pack(side=tk.RIGHT,fill=tk.BOTH) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
    md_enter.pack(fill=tk.Y) # 将文本框填充进窗口
    # 将滚动条与文本框关联
    scroll.config(command=md_enter.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
    md_enter.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框
    post_btn=ttk.Button(md_win,text='发布',command=lambda:md_post(md_enter.get(),name_enter.get(),title_enter.get(),linkedRepo_enter.get())).pack(side=tk.BOTTOM,fill=tk.X)
    md_win.mainloop()

def init():
    global user
    c=msgbox.askokcancel(title = '要继续吗？',message='初始化博客站点将会覆盖以前的所有数据，要继续吗？')
    if c:
        site_dir=filebox.askdirectory(title='选择本地博客站点备份并上传')
        print(site_dir)
        root,dirs,files=os.walk(file)
        msgbox.showinfo('进行以下操作','手动清空（或创建）名为“你的用户名.github.io”的存储库，然后单击确定以继续。')
        for path in files:
            with open(site_dir+path,'rb') as f:
                content=f.read()
                upload_file(content,path,user,user+".github.io","/")

def settings():
    settings=tk.Tk()
    settings.title('设置')
    settings.state("zoomed")
    # 创建画布
    about=ttk.LabelFrame(settings,text='关于')
    about.pack(padx=10,pady=10,fill=tk.X)
    tk.Label(about,text='One Blogger 2',font=('幼圆',12)).pack(pady=5)
    tk.Label(about,text='2020 By 人工智障',font=('幼圆',12)).pack(pady=5)
    tk.Label(about,text='V 2.1.0',font=('幼圆',12)).pack(pady=5)
    ttk.Button(about,text='作者博客',command=lambda:webbrowser.open("https://www.cnblogs.com/TotoWang/")).pack(pady=5,padx=5)
    api=ttk.LabelFrame(settings,text='API参数设置')
    api.pack(padx=10,pady=10,fill=tk.X)
    ttk.Label(api,text='GitHub Token').pack(pady=10)
    token_enter=ttk.Entry(api)
    token_enter.pack(padx=30,fill=tk.X)
    ttk.Label(api,text='GitHub用户名').pack(pady=10)
    user_enter=ttk.Entry(api)
    user_enter.pack(padx=30,fill=tk.X)
    ttk.Label(api,text='GitHub账户邮箱').pack(pady=10)
    email_enter=ttk.Entry(api)
    email_enter.pack(padx=30,fill=tk.X)
    ttk.Button(api,text='保存',command=writeToken).pack(pady=20)
    ui=ttk.LabelFrame(settings,text='外观')
    ui.pack(padx=10,pady=10,fill=tk.X)
    ttk.Label(ui,text='敬请期待').pack(pady=10)
    site=ttk.LabelFrame(settings,text='站点设置')
    site.pack(padx=10,pady=10,fill=tk.X)
    ttk.Button(site,text="初始化博客站点",command=init).pack(padx=10,pady=10,fill=tk.X)
    settings.mainloop()

s_win=tk.Tk()
s_win.title('One Blogger')

screenWidth = s_win.winfo_screenwidth()  # 获取显示区域的宽度
screenHeight = s_win.winfo_screenheight()  # 获取显示区域的高度
width = 300  # 设定窗口宽度
height = 165  # 设定窗口高度
left = (screenWidth - width) / 2
top = (screenHeight - height) / 2
s_win.geometry("%dx%d+%d+%d" % (width, height, left, top))
s_win.resizable(0,0)
s_win.overrideredirect(1)

titleA=tk.Label(s_win,text='One Blogger 2',font=('courier new',25))
titleA.pack(pady=20)

titleB=tk.Label(s_win,text='博客后台',font=('幼圆',15))
titleB.pack(pady=10)

ver=tk.Label(s_win,text='后台版本 V2.1.0',font=('幼圆',10))
ver.pack(pady=10)

s_win.update()

time.sleep(2)
s_win.destroy()

if token=='' or user=='' or email=='':
    token_win=tk.Tk()
    token_win.geometry('300x500')
    token_win.title('One Blogger')
    token_win.resizable(0,0)
    s = ttk.Style()
    print(s.theme_names()) #ttk所有主题风格[windows Python 3.8.3 tk 8.6.9]
    #output:('winnative','clam','alt','default','classic','vista','xpnative')
    s.theme_use('vista')
    tk.Label(token_win,text='输入一些必需的信息以继续',font=('幼圆',15)).pack(pady=20)
    tk.Label(token_win,text='GitHub Token',font=('幼圆',10)).pack(pady=10)
    token_enter=ttk.Entry(token_win)
    token_enter.pack(padx=30,fill=tk.X)
    tk.Label(token_win,text='GitHub用户名',font=('幼圆',10)).pack(pady=10)
    user_enter=ttk.Entry(token_win)
    user_enter.pack(padx=30,fill=tk.X)
    tk.Label(token_win,text='GitHub账户邮箱',font=('幼圆',10)).pack(pady=10)
    email_enter=ttk.Entry(token_win)
    email_enter.pack(padx=30,fill=tk.X)
    ttk.Button(token_win,text='继续',command=writeToken).pack(pady=20)
    token_win.mainloop()


win=tk.Tk()
win.geometry('800x450')
win.title('One Blogger')

s = ttk.Style()
print(s.theme_names()) #ttk所有主题风格[windows Python 3.8.3 tk 8.6.9]
#output:('winnative','clam','alt','default','classic','vista','xpnative')
s.theme_use('clam')

ttk.Separator(win,orient=tk.HORIZONTAL).pack(pady=7,fill=tk.X)
ttk.Button(win,text="MarkDown编辑器",command=md).pack(padx=10,fill=tk.X)
ttk.Separator(win,orient=tk.HORIZONTAL).pack(pady=7,fill=tk.X)
ttk.Button(win,text="初始化博客站点",command=init).pack(padx=10,fill=tk.X)
ttk.Button(win,text="设置",command=settings).pack(padx=10,fill=tk.X)

win.mainloop()
