from customtkinter import *

class Main(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.frame=CTkFrame(self, width=200, height=300)
        self.frame.pack_propagate(False)
        self.frame.configure(width=0)
        self.frame.place(x=0,y=0)
        self.is_show_menu = False
        self.frame_width = 0
        self.label = CTkLabel(self.frame, text="Введіть ім'я")
        self.label.pack(pady=30)
        self.entry = CTkEntry(self.frame)
        self.entry.pack()
        self.label_theme = CTkOptionMenu(self.frame,values=["Темна", "Світла"],command=self.change_theme)
        self.label_theme.pack(side="bottom",pady=20)
        self.btn = CTkButton(self,text="PRESS", width=30)
        self.btn.place(x=0,y=0)
        self.menu_show_speed = 20
        self.chat_text = CTkTextbox(self, state="disable")
        self.chat_text.place(x=0, y=30)
        self.message_input = CTkEntry(self,placeholder_text="Введіть повідомлення")
        self.message_input.place(x=0,y=250)
        self.send_button = CTkButton(self, text="SEND",width=30)
        self.send_button.place(x=200,y=250)
        self.username="Andrii"
        self.adaptive_ui()


    def show_menu(self):
        if self.frame_width<=200:
            self.frame_width+= self.menu_show_speed
            self.frame.configure(width=self.frame_width, height=300)
            if self.frame_width >=30:
                self.btn.configure(width= self.frame_width, text="PRESS")
        if self.is_show_menu:
            self.after(20,self.show_menu)

    def close_menu(self):
        if self.frame_width>=0:
            self.frame_width -= self.menu_show_speed
            self.frame.configure(width=self.frame_width)
            if self.frame_width:>30


    def adaptive_ui(self):
        self.chat_text.configure(width=self.winfo_width()-self.frame.winfo_width(), height=self.winfo_height()-self.message_input()-30)
        self.chat_text.place(x=self.frame.winfo_width()-1)


        self.message_input.configure(width=self.winfo_width()-self.frame.winfo_width()-self.send_button.winfo_width)
        self.message_input.place(x=self.winfo_width(), y=self.winfo_height()-self.send_button.winfo_height())
        self.button.place(x=self.winfo_width()-self.send_button.winfo_width(), y=self.winfo_height()-self.send_button.winfo_height())
        self.after(20,self.adaptive_ui)


    def add_message(self, text):
        self.chat_text.configure(state="normal")
        self.chat_text.insert(END, "Я: "+ text+"\n")
        self.chat_text.configure(state="disable")

    def send_message(self):
        message = self.entry.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.enrty.delete(0,END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer+=chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >=3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author} {message}")
        elif msg_type == "IMAGE":
            author = parts[1]
            filename = parts[2]
            self.add_message(f"{author} {filename}")





















win = Main()
win.mainloop()