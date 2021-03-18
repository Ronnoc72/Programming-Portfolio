from tkinter import ttk
from tkinter import *
from tkinter.font import families

HEIGHT = 350
WIDTH = 600
TITLE = "Calculator"
BACKGROUND = "darkgray"
FONT = ("Palatino Linotype", 16)


class App(Frame):
    def __init__(self, master):
        super(App, self).__init__(master)
        self.num_list = []
        self.answer = 0
        self.first_num = 0
        self.second_num = 0
        self.btn_style = ttk.Style()
        self.btn_style.configure("btn.TButton", background="#80b0ff", foreground="black", padding=10,
                                 font=FONT)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.screen = Label(self, width=45, height=2, background="yellow", font=FONT, anchor=E)
        self.widget = Label(self, text="", font=('helvetica', 16), background="yellow")
        ttk.Button(self, style="btn.TButton", text="1", command=lambda: self.handle_click('1')).grid(row=1, column=0)
        ttk.Button(self, style="btn.TButton", text="2", command=lambda: self.handle_click('2')).grid(row=1, column=1)
        ttk.Button(self, style="btn.TButton", text="3", command=lambda: self.handle_click('3')).grid(row=1, column=2)
        ttk.Button(self, style="btn.TButton", text="+", command=lambda: self.handle_click('+')).grid(row=1, column=3)
        ttk.Button(self, style="btn.TButton", text="4", command=lambda: self.handle_click('4')).grid(row=2, column=0)
        ttk.Button(self, style="btn.TButton", text="5", command=lambda: self.handle_click('5')).grid(row=2, column=1)
        ttk.Button(self, style="btn.TButton", text="6", command=lambda: self.handle_click('6')).grid(row=2, column=2)
        ttk.Button(self, style="btn.TButton", text="-", command=lambda: self.handle_click('-')).grid(row=2, column=3)
        ttk.Button(self, style="btn.TButton", text="7", command=lambda: self.handle_click('7')).grid(row=3, column=0)
        ttk.Button(self, style="btn.TButton", text="8", command=lambda: self.handle_click('8')).grid(row=3, column=1)
        ttk.Button(self, style="btn.TButton", text="9", command=lambda: self.handle_click('9')).grid(row=3, column=2)
        ttk.Button(self, style="btn.TButton", text="x", command=lambda: self.handle_click('x')).grid(row=3, column=3)
        ttk.Button(self, style="btn.TButton", text=".", command=lambda: self.handle_click('.')).grid(row=4, column=0)
        ttk.Button(self, style="btn.TButton", text="0", command=lambda: self.handle_click('0')).grid(row=4, column=1)
        ttk.Button(self, style="btn.TButton", text="C", command=lambda: self.handle_click('C')).grid(row=4, column=2)
        ttk.Button(self, style="btn.TButton", text="/", command=lambda: self.handle_click('/')).grid(row=4, column=3)
        ttk.Button(self, style="btn.TButton", text="=", command=lambda: self.handle_click('='), width=52)\
            .grid(row=5, column=0, columnspan=4)
        self.screen.grid(row=0, column=0, columnspan=4)
        self.widget.place(x=10, y=10)

    def handle_click(self, btn_id):
        if btn_id == '+' or btn_id == '-' or btn_id == 'x' or btn_id == '/':
            self.widget['text'] = btn_id
            if not self.first_num:
                self.first_num = float(''.join(self.num_list))
                self.num_list.clear()
        if self.first_num and btn_id == '=' and self.num_list:
            if self.widget['text'] == '+':
                self.second_num = float(''.join(self.num_list))
                self.answer = self.first_num + self.second_num
            elif self.widget['text'] == '-':
                self.second_num = float(''.join(self.num_list))
                self.answer = self.first_num - self.second_num
            elif self.widget['text'] == 'x':
                self.second_num = float(''.join(self.num_list))
                self.answer = self.first_num * self.second_num
            elif self.widget['text'] == '/':
                self.second_num = float(''.join(self.num_list))
                self.answer = self.first_num / self.second_num
            self.screen['text'] = str(self.answer)
        if btn_id.isdigit() or btn_id == '.':
            self.num_list.append(btn_id)
        if btn_id == 'C':
            self.num_list.clear()
            self.first_num = 0
            self.second_num = 0
            self.answer = 0
            self.widget['text'] = ''
        self.screen['text'] = ''.join(self.num_list)
        if self.answer:
            self.screen['text'] = float(self.answer)
            self.widget['text'] = ''
            self.num_list.clear()
            self.first_num = float(self.answer)
            self.second_num = 0
            self.answer = 0


def main():
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title(TITLE)
    root.config(bg=BACKGROUND)
    App(root)
    # for family in families():
    #     print(family)
    root.mainloop()


main()
