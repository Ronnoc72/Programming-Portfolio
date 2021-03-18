# Connor Paxman
# trying to make a cool looking gui in tkinter.
# 1 / 29 / 21

# imports
from tkinter import ttk
from tkinter import *
from tkinter import font

HEIGHT = 650
WIDTH = 400

class HomePageElement:
    """an element on the home page that controls the infromation sent to the create_page_routine."""
    def __init__(self, master, file, index):
        self.master = master
        self.file = file
        self.index = index
        self.font = ('Franklin Gothic Medium', 18)
        self.large_font = ('Franklin Gothic Medium', 24)
        self.small_font = ('Franklin Gothic Medium', 14)
        self.smaller_font = ('Franklin Gothic Medium', 12)
        self.create_element()

    def load(self):
        """sents the information to the the create routine page."""
        for child in self.master.winfo_children():
            child.destroy()
        home_page.handle_click(self.master, loading=True, file=self.file)

    def create_element(self):
        """loads all the physical elements on the page placing the element on the center of the screen."""
        self.btn = Button(root.master, text=self.file, command=self.load, font=self.font, borderwidth=0, background="#80b0ff")
        self.btn.place(x=WIDTH/6, y=(self.index*55)+75, height=50, width=WIDTH/1.5)


class EntryBox:
    """An induvidual entry box that the user sets an event to."""
    def __init__(self, master, entry_index, info):
        self.master = master
        self.entry_index = entry_index
        if info == []:
            self.info_list = ["", "", "", "", "False", ""]
        else:
            self.info_list = info
        self.position = 0
        self.spacing = 0
        self.check = self.info_list[4] == "True"
        self.font = ('Franklin Gothic Medium', 18)
        self.large_font = ('Franklin Gothic Medium', 24)
        self.small_font = ('Franklin Gothic Medium', 12)
        self.smaller_font = ('Franklin Gothic Medium', 10)
        self.create_entry()

    def checked(self):
        """handles when the user checkes the checkbox indicating the user that the event has been checked off."""
        if not self.check:
            new_text = ""
            for i in range(len(self.lbl_event_title["text"])):
                new_text += self.lbl_event_title["text"][i] + u"\u0336"
            self.lbl_event_title["text"] = new_text
            self.check = True
        else:
            self.lbl_event_title["text"] = f"Event {self.entry_index+1}"
            self.check = False

    def update_checked(self):
        """updates the check button due to if the check variable is toggled"""
        if self.check:
            new_text = ""
            for i in range(len(self.lbl_event_title["text"])):
                new_text += self.lbl_event_title["text"][i] + u"\u0336"
            self.lbl_event_title["text"] = new_text

    def remove_entry(self):
        """removes the entry"""
        self.entry_frame.destroy()
        CreateRoutinePage.update_entries(home_page.routine_page, self.entry_index)

    def update_entry(self, pos=-1):
        """updates the position of the entry box."""
        if pos == -1:
            self.entry_index -= 1
        else:
             self.position += pos
        self.spacing = 0
        self.entry_frame.destroy()
        self.create_entry()

    def create_entry(self):
        """creates an entry on the position given to it."""
        self.entry_frame = Frame(self.master, background="blue")
        self.lbl_top = Label(self.entry_frame)
        self.lbl_bottom = Label(self.entry_frame)
        # title data
        self.lbl_event_title = Label(self.entry_frame, text=f"Event {self.entry_index+1}", font=self.font)
        self.lbl_event_title.pack(fill="x")
        self.btn_remove = Button(self.lbl_event_title, text="X", font=self.smaller_font, command=self.remove_entry)
        self.btn_remove.pack(anchor="e")
        self.lbl_title = Label(self.lbl_top, text="Title", font=self.small_font)
        self.text_event = Text(self.lbl_top, borderwidth=0, width=18, height=1, font=self.smaller_font)
        self.text_event.insert(0.0, self.info_list[1])
        # date data
        self.lbl_date = Label(self.lbl_top, text="Date", font=self.small_font)
        self.text_date = Text(self.lbl_top, borderwidth=0, width=18, height=1, font=self.smaller_font)
        self.text_date.insert(0.0, self.info_list[2])
        # entry description
        self.lbl_des = Label(self.lbl_bottom, text="Description", font=self.small_font)
        self.text_des = Text(self.lbl_bottom, borderwidth=0, width=23, height=2, font=self.smaller_font)
        self.text_des.insert(0.0, self.info_list[3])
        # adding the informaiton to the entry list.
        self.int_var = IntVar()
        # check box
        checkbox = Checkbutton(self.lbl_bottom, text="Finished", font=self.small_font, variable=self.int_var, command=self.checked)
        checkbox.grid(column=1, row=0, rowspan=2)
        if self.check:
            checkbox.toggle()
        self.update_checked()
        # setting the text
        self.lbl_title.grid(column=0, row=0)
        self.lbl_date.grid(column=1, row=0)
        self.lbl_des.grid(column=0, row=0)
        self.text_event.grid(column=0, row=1)
        self.text_date.grid(column=1, row=1)
        self.text_des.grid(column=0, row=1)
        self.lbl_top.pack(anchor="n")
        self.lbl_bottom.pack(anchor="s", ipadx=9)
        for i in range(self.entry_index+1):
            if (i)%3 == 0 and (i) >= 3:
                self.spacing += 1
        self.entry_frame.place(x=20, y=(self.entry_index * 160) + 90 + self.position + (self.spacing*170), width=int(WIDTH - 40), height=150)


class CreateRoutinePage:
    """the page that the user goes to for creating a routine"""
    def __init__(self, master, loading=False, file=""):
        self.root = master
        self.name = file
        self.index = 0
        self.scroll_index = 0
        self.entries = []
        self.font = ('Franklin Gothic Medium', 18)
        self.large_font = ('Franklin Gothic Medium', 24)
        self.small_font = ('Franklin Gothic Medium', 14)
        self.smaller_font = ('Franklin Gothic Medium', 12)
        self.smallest_font = ('Franklin Gothic Medium', 8)
        for child in self.root.winfo_children():
            child.destroy()
        if not loading:
            self.name_routine()
        else:
            self.create_widgets(file)

    def key_press(self, e):
        """triggers the next screen when the enter key is pressed."""
        if e.keycode == 13:
            text = self.name_text.get(0.0, END)
            for i in range(len(text)-2):
                self.name += text[i]
            self.name_text.delete(0.0, END)
            for child in self.root.winfo_children():
                child.destroy()
            self.create_widgets()

    def btn_press(self):
        """triggers the next screen when the 'create routine' button is pressed."""
        text = self.name_text.get(0.0, END)
        for i in range(len(text)-1):
            self.name += text[i]
        self.name_text.delete(0.0, END)
        for child in self.root.winfo_children():
            child.destroy()
        self.create_widgets()

    def exit_name_routine(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.cvs = Canvas(root, width=405, height=655, highlightbackground="lightblue")
        self.cvs.pack()
        MyCanvas(self.cvs)
        home_page.__init__(self.root, text)

    def name_routine(self):
        """the widgets that create the screen displaying what the user will name its routine."""
        self.root.bind_all("<Key>", self.key_press)
        self.root["bg"] = "lightblue"
        self.label = Label(self.root, height=int(HEIGHT * 1.5), width=WIDTH, background="lightblue", highlightbackground="white")
        self.create_btn = Button(self.label, text="Create Routine", width=13, height=1, background="#80b0ff", borderwidth=0, font=self.font, command=self.btn_press)
        self.name_text = Text(self.label, width=15, height=1, font=self.large_font, borderwidth=0)
        self.back_btn = Button(self.root, font=self.large_font, borderwidth=0, command=self.exit_name_routine, text="Back", background="#80b0ff")
        self.back_btn.place(x=WIDTH/3, y=HEIGHT-35, width=WIDTH/3, height=30)
        self.name_text.pack(anchor="center")
        self.create_btn.pack(anchor="center", pady=5)
        self.label.pack(anchor="center", pady=260)

    def update_scroll(self, pos):
        """updates the scroll with all of the entries."""
        if pos > 0:
            if self.scroll_index >= 0:
                return
            self.scroll_index += 1
        else:
            self.scroll_index -= 1
        if self.scroll_index == 0:
            self.entry_btn = Button(self.root, background="white", command=self.create_entry, text="Create Entry", font=self.smallest_font)
            self.back_btn = Button(self.root, background="white", command=self.save_entries, text="Back", font=self.smallest_font)
            self.entry_btn.place(x=5, y=5, width=75)
            self.back_btn.place(x=WIDTH-80, y=5, width=75)
        else:
            self.entry_btn.destroy()
            self.back_btn.destroy()
        for i in range(len(self.entries)):
            self.entries[i].update_entry(pos)

    def save_entries(self):
        """saves all the data of all the entries in a file in text_data, having the name of the routine."""
        if self.name:
            file = open("./text_data/"+self.name+".txt", 'w')
            for entry in self.entries:
                text = "<!--ENTRY--!>\n"
                for child in entry.entry_frame.winfo_children():
                    if len(child.winfo_children()) == 4:
                        text += child.winfo_children()[1].get(0.0, END)
                        text += child.winfo_children()[3].get(0.0, END)
                    elif len(child.winfo_children()) == 3:
                        text += child.winfo_children()[1].get(0.0, END)
                        if entry.int_var.get() == 1:
                            text += "True\n"
                        else:
                            text += "False\n"
                file.write(text)
            file.close()
        for child in self.root.winfo_children():
            child.destroy()
        temp_canvas = Canvas(root, width=405, height=655, highlightbackground="lightblue")
        temp_canvas.pack()
        routine_names = open("./routine_names.txt.txt", 'r')
        display_canvas.__init__(temp_canvas)
        file_text = routine_names.read().split(",")
        if self.name not in file_text:
            routine_names.close()
            routine_names = open("./routine_names.txt.txt", 'a')
            routine_names.write(self.name+',')
            file_text[len(file_text)-1] = self.name
            file_text.append("")
            routine_names.close()
        home_page.__init__(self.root, file_text)
        routine_names.close()

    def create_widgets(self, file=[]):
        """creates the front page for all the entries to be displayed on."""
        self.root.unbind_all("<Key>")
        self.canvas = Canvas(self.root, width=WIDTH, height=HEIGHT + 300, highlightbackground="lightblue", background="#80b0ff")
        self.canvas.create_rectangle(10, 10, 390, 640, outline="", fill="lightblue")
        self.canvas.create_rectangle(20, 20, 380, 60, outline="", fill="cornflowerblue")
        self.canvas.create_text(WIDTH/2, 47, text=self.name, font=self.font)
        self.scroll_btn = Button(self.canvas, text="\/", width=WIDTH//10, borderwidth=0, background="cornflowerblue", command=lambda: self.update_scroll(-HEIGHT))
        self.top_scroll_btn = Button(self.canvas, text="/\\", width=WIDTH//10, borderwidth=0, background="cornflowerblue", command=lambda: self.update_scroll(HEIGHT))
        self.scroll_btn.place(x=WIDTH/7, y=HEIGHT/1.07)
        self.top_scroll_btn.place(x=WIDTH/7, y=55)
        self.entry_btn = Button(self.root, background="white", command=self.create_entry, text="Create Entry", font=self.smallest_font)
        self.back_btn = Button(self.root, background="white", command=self.save_entries, text="Back", font=self.smallest_font)
        if file:
            temp_file = open("./text_data/"+file+".txt", 'r')
            file_text = temp_file.read()
            split_file = file_text.split("<!--ENTRY--!>")
            for i in range(len(split_file)):
                if split_file[i] == "":
                    continue
                temp = split_file[i].split('\n')
                self.create_entry(temp)
        self.back_btn.place(x=WIDTH-80, y=5, width=75)
        self.entry_btn.place(x=5, y=5, width=75)
        self.canvas.pack()
       
    def create_entry(self, information=[]):
        """creates a frame that is a single event for the user's routine."""
        entry = EntryBox(self.canvas, self.index, information)
        self.entries.append(entry)
        self.index += 1

    def update_entries(self, entry_index):
        """removes entries and updates them accordingly."""
        self.entries.remove(self.entries[entry_index])
        self.index -= 1
        for i in range(len(self.entries)):
            if entry_index < self.entries[i].entry_index:
                self.entries[i].update_entry()


class HomePage:
    """The main component with the list of routines"""
    def __init__(self, master, files):
        self.files = files
        self.file_elements = []
        self.root = master
        self.create_widgets()

    def create_widgets(self):
        """creates all the home_page_element for the page and the create routine button."""
        self.add_btn = Canvas(self.root, width=147, height=125, background="lightblue", highlightbackground="lightblue")
        self.add_btn.create_oval(2, 2, 148, 152, fill="#80b0ff", outline="", tag="add-btn")
        self.add_btn.create_rectangle(0, 75, 200, 200, fill="#80b0ff", width=2)
        self.add_btn.create_text(147/2, 100/2, text="+", font=("Bahnschrift Light SemiCondensed", 36))
        self.add_btn.place(x=124, y=HEIGHT-85)
        for i in range(len(self.files)-1):
            file_element = HomePageElement(self.root, self.files[i], i)
            self.file_elements.append(file_element)
        self.add_btn.bind("<Button-1>", self.handle_click)
        self.add_btn.bind("<Enter>", self.on_enter)
        self.add_btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """controls when the user is going to click on the create_routine button and indicates with highlighting."""
        self.add_btn.delete(ALL)
        self.add_btn.create_oval(2, 2, 148, 152, fill="red", outline="", tag="add-btn")
        self.add_btn.create_rectangle(0, 75, 200, 200, fill="#80b0ff", width=2)
        self.add_btn.create_text(147/2, 100/2, text="+", font=("Bahnschrift Light SemiCondensed", 36))

    def on_leave(self, e):
        """When the user exits the create routine button."""
        self.add_btn.delete(ALL)
        self.add_btn.create_oval(2, 2, 148, 152, fill="#80b0ff", outline="", tag="add-btn")
        self.add_btn.create_rectangle(0, 75, 200, 200, fill="#80b0ff", width=2)
        self.add_btn.create_text(147/2, 100/2, text="+", font=("Bahnschrift Light SemiCondensed", 36))

    def handle_click(self, e, loading=False, file=""):
        """create a new routine page if the user clicked the create routine button."""
        self.routine_page = CreateRoutinePage(self.root, loading, file)

class MyCanvas:
    """The canvas that layers under the home page widgets."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.config(background="#80b0ff")
        self.create_shapes()

    def create_shapes(self):
        """all of the shapes created by the canvas"""
        # the outline of the entire outside.
        self.canvas.create_rectangle(10, 10, 390, 640, outline="", fill="lightblue")
        # button that adds an event
        self.canvas.create_rectangle(0, 0, 400, 40, outline="", fill="#80b0ff")
        # rect that is around the inside of the window
        self.canvas.create_rectangle(10, 40, 390, 640, outline="black", width=2)
        # lines going through the title.
        self.canvas.create_line(100, 20, 130, 20, width=3)
        self.canvas.create_line(270, 20, 300, 20, width=3)
        # title text.
        self.canvas.create_text(200, 17, font=("Bahnschrift Light SemiCondensed", 20), text="Routine App")
        # button at the bottom of page text.
        # self.canvas.create_text(200, 615, font=("Bahnschrift Light SemiCondensed", 60), text="+")


root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Routine App")
root.resizable(False, False)

text = ""
routine_names_file = open("./routine_names.txt.txt", 'r')
text = routine_names_file.read().split(",")
routine_names_file.close()

my_canvas = Canvas(root, width=405, height=655, highlightbackground="lightblue")
my_canvas.pack()

display_canvas = MyCanvas(my_canvas)
home_page = HomePage(root, text)

root.mainloop()
