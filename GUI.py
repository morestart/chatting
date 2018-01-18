import pickle
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import socket
import threading
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def show_about_info():
    messagebox.showinfo("关于", "版权所有:3406实验室Girls团队")


class Chat(object):
    def __init__(self):
        self.IP = "192.168.1.105"

        self.PORT = 9999

        self.window = Tk()
        self.window.title("3406聊天室")
        frame = Frame(self.window).pack()

        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (300 / 2))
        y = int((hs / 2) - (300 / 2))
        self.window.geometry("{}x{}+{}+{}".format(500, 350, x, y))
        self.window.resizable(0, 0)

        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)
        about_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="选项", menu=about_menu)
        about_menu.add_command(label="关于", command=show_about_info)

        self.text = Text(frame)
        self.text.pack(anchor=W)
        self.text.configure(state="disabled")
        self.entry = Entry(frame)
        self.entry.pack(side=LEFT, expand=YES, fill=X, anchor=W)
        self.entry.focus_force()
        self.entry.bind("<Return>", self.send_data)
        self.button = Button(frame, text="发送", command=self.send_data)
        self.button.pack(side=RIGHT, anchor=W)

        self.conn()
        self.send_threading = threading.Thread(target=self.send_data, args=(1,))
        self.recive_threading = threading.Thread(target=self.recive_data)
        self.send_threading.setDaemon(True)
        self.recive_threading.setDaemon(True)
        self.send_threading.start()
        self.recive_threading.start()

        self.window.mainloop()

    def conn(self):
        try:
            s.connect((self.IP, self.PORT))
        except:
            messagebox.showerror("Error", "错误,服务器未开启!")
            self.window.destroy()

    def recive_data(self):
        # global name
        while True:
            data = s.recv(1024)
            data = data.decode("utf-8")
            print(data)

            self.text.configure(state="normal")
            self.text.insert(END, data + "\n")
            self.text.see(END)
            self.text.configure(state="disabled")

    def send_data(self, event):
        try:
            data = self.entry.get()
            # print(data)
            if data is not None:
                if os.path.exists("name.txt"):
                    with open("name.txt", "r") as f:
                        name = f.read()
                        data = name + ":" + data
                        s.send(data.encode("utf-8"))
                        self.entry.delete(0, 'end')

        except:
            messagebox.showerror("Error", "错误,服务器未开启!")
            quit(1)


class Account(object):
    def __init__(self):
        self.window = Tk()
        self.window.title("登陆")
        self.window.geometry("450x300")
        canvas = Canvas(self.window, height=200, width=500)
        image_file = PhotoImage(file="welcome.gif")
        canvas.create_image(0, 0, anchor="nw", image=image_file)
        canvas.pack(side="top")

        Label(self.window, text="用户名:").place(x=50, y=150)
        Label(self.window, text="密码:").place(x=50, y=190)

        self.usr_name = StringVar()
        self.usr_name.set("在此输入用户名")
        self.entry_name = Entry(self.window, textvariable=self.usr_name)
        self.entry_name.place(x="160", y="150")

        self.usr_pwd = StringVar()
        self.entry_pwd = Entry(self.window, textvariable=self.usr_pwd, show="*")
        self.entry_pwd.place(x=160, y=190)

        btn_login = Button(self.window, text="登陆", command=self.usr_login)
        btn_login.place(x=170, y=230)
        btn_sign_up = Button(self.window, text="注册", command=self.usr_sign_up)
        btn_sign_up.place(x=270, y=230)

        self.window.mainloop()

    def usr_login(self):
        usr_name = self.usr_name.get()
        usr_pwd = self.usr_pwd.get()
        with open("name.txt", "wb") as f:
            f.write(self.entry_name.get().encode("gbk"))
        try:
            with open('usrs_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usrs_info.pickle', 'wb') as usr_file:
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)
        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                # messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
                self.window.destroy()
                Chat()
            else:
                messagebox.showerror(message='密码错误,请重试')
        else:
            is_sign_up = messagebox.askyesno('Welcome', '用户未注册,是否注册?')
            if is_sign_up:
                self.usr_sign_up()

    def usr_sign_up(self):
        def sign_to():
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            try:
                with open("usrs_info.pickle", "rb") as usr_file:
                    exist_usr_info = pickle.load(usr_file)
                if np != npf:
                    messagebox.showerror("Error", "密码必须相同!")
                elif nn in exist_usr_info:
                    messagebox.showerror("Error", "用户已注册!")
                else:
                    exist_usr_info[nn] = np
                    with open("usrs_info.pickle", "wb") as usr_file:
                        pickle.dump(exist_usr_info, usr_file)
                    messagebox.showinfo("Welcome", "注册成功!")
                    window_sign_up.destroy()

            except FileNotFoundError:
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usrs_info = {'admin': 'admin'}
                    pickle.dump(usrs_info, usr_file)

        window_sign_up = Toplevel(self.window)
        window_sign_up.geometry("350x200")
        window_sign_up.title("Sign up window")

        new_name = StringVar()
        new_name.set("example@python.com")
        Label(window_sign_up, text="用户名: ").place(x=10, y=10)
        entry_new_name = Entry(window_sign_up, textvariable=new_name)
        entry_new_name.place(x=150, y=10)

        new_pwd = StringVar()
        Label(window_sign_up, text="密码: ").place(x=10, y=50)
        entry_usr_pwd = Entry(window_sign_up, textvariable=new_pwd, show="*")
        entry_usr_pwd.place(x=150, y=50)

        new_pwd_confirm = StringVar()
        Label(window_sign_up, text="确认密码: ").place(x=10, y=90)
        entry_usr_pwd_confirm = Entry(window_sign_up, textvariable=new_pwd_confirm, show="*")
        entry_usr_pwd_confirm.place(x=150, y=90)

        btn_comfirm_sign_up = Button(window_sign_up, text="注册", command=sign_to)
        btn_comfirm_sign_up.place(x=150, y=130)


if __name__ == '__main__':
    # Account()
    Chat()
