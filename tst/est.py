from tkinter import *
from tkinter.ttk import Combobox

root = Tk()
root.minsize(500,300)
root.maxsize(550,310)

class MyListbox:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.closes)

        self.myData= (
            ["1", "Jhon Doe", "Madrid", "0341-672541", "6 SD"],
            ["2", "Mike Grant", "Barcelona", "0341-435271", "7 SD"],
            ["3", "Steven Mc Fly", "Rome", "0341-123456", "8 SD"],
            ["4", "Joao Pontes", "Rio", "0341-234567", "9 SD"],
            ["7", "Kenji S.", "Tokyo", "0341-213212", "10 SD"])

        self.establishment()

    def combobox_handler(self, event):
        current = self.combobox.current()
        self.entNumber.delete(0, END)
        self.entName.delete(0, END)
        self.entCity.delete(0, END)
        self.entTel.delete(0, END)
        self.entAddress.delete(0, END)

        self.entNumber.insert(END, self.myData[current][0])
        self.entName.insert(END, self.myData[current][1])
        self.entCity.insert(END, self.myData[current][2])
        self.entTel.insert(END, self.myData[current][3])
        self.entAddress.insert(END, self.myData[current][4])

    def establishment(self):
        mainFrame = Frame(self.parent)
        mainFrame.pack(fill=BOTH, expand=YES)

        self.statusBar = Label(mainFrame, text="App",relief=SUNKEN, bd=1)
        self.statusBar.pack(side=BOTTOM, fill=X)

        fr_left = Frame(mainFrame, bd=10)
        fr_left.pack(fill=BOTH, expand=YES, side=LEFT)

        names = [person[1] for person in self.myData]
        self.combobox = Combobox(fr_left, values=names)
        self.combobox.bind('<<ComboboxSelected>>', self.combobox_handler)
        self.combobox.pack()

        fr_right = Frame(mainFrame, bd=10)
        fr_right.pack(fill=BOTH, expand=YES, side=RIGHT)

        fr_up = Frame(fr_right)
        fr_up.pack(side=TOP, expand=YES)

        Label(fr_up, text='List Number').grid(row=0, column=0, sticky=W)
        self.entNumber = Entry(fr_up)
        self.entNumber.grid(row=0, column=1)

        Label(fr_up, text='Name').grid(row=1, column=0, sticky=W)
        self.entName = Entry(fr_up)
        self.entName.grid(row=1, column=1)

        Label(fr_up, text='City').grid(row=2, column=0, sticky=W)
        self.entCity = Entry(fr_up)
        self.entCity.grid(row=2, column=1)

        Label(fr_up, text='No. Tel').grid(row=3, column=0, sticky=W)
        self.entTel = Entry(fr_up)
        self.entTel.grid(row=3, column=1)

        Label(fr_up, text='Address').grid(row=4, column=0, sticky=W)
        self.entAddress = Entry(fr_up)
        self.entAddress.grid(row=4, column=1)

    def closes(self, event=None):
        self.parent.destroy()

if __name__ == '__main__':
    app = MyListbox(root, "Main Window")
    root.mainloop()
