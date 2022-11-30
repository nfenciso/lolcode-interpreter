import os
import tkinter as tk
from tkinter import Frame, OptionMenu, Scrollbar, StringVar, messagebox
from tkinter import filedialog as fd
from tkinter.font import Font

class GUI:
    def __init__(self):
        pass



root = tk.Tk()

class GUI:
    def __init__(self, master):
        master.geometry("1200x700")
        master.resizable(False, False)

        frame1 = Frame(master)

        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)

        # ===================== lol code frame ==========================
        lolcode_frame = Frame(frame1, background="#272727")
        # lolcode_label = tk.Label(lolcode_frame, text="Code section", font=('Arial', 10))
        # lolcode_label.pack()
        berlin_sans = Font(family='Berlin Sans', size=10, weight='bold')
        btn2 = tk.Button(lolcode_frame, text="Upload LOL code file", font=berlin_sans, width = 43, command=self.open_file)
        btn2.pack(pady=(10, 5))

        # v=tk.Scrollbar("win", orient='vertical')
        # v.pack(side="RIGHT", fill='y')

        consolas_font = Font(family='Rockwell', size=10, weight='normal')
        self.code_textbox = tk.Text(lolcode_frame, height=20, width=50, font=consolas_font, bg="#DADADA")
        self.code_textbox.pack(padx=10, pady=(0, 10))

        lolcode_frame.grid(row=0, column=0, sticky="nsew")

        # ===================== lexemes frame ==========================
        lexemes_frame = Frame(frame1, background="#272727")
        lexemes_label = tk.Label(lexemes_frame, text="Lexemes section", font=('Arial', 10))
        lexemes_label.pack()
        self.lexemes_textbox = tk.Text(lexemes_frame, height=20, width=40, font=('Arial', 10))
        self.lexemes_textbox.pack(padx=10, pady=10)
        lexemes_frame.grid(row=0, column=1, sticky="nsew")

        # ===================== symbol table frame ==========================
        symbol_table_frame = Frame(frame1, background="#272727")
        symbol_table_label = tk.Label(symbol_table_frame, text="Symbol Table section", font=('Arial', 10))
        symbol_table_label.pack()
        self.symbol_table_textbox = tk.Text(symbol_table_frame, height=20, width=40, font=('Arial', 10))
        self.symbol_table_textbox.pack(padx=10, pady=10)
        symbol_table_frame.grid(row=0, column=2, sticky="nsew")

        frame1.pack(expand=True, fill="both", padx=10, pady=10)

        # ===================== execute frame ==========================
        frame2 = Frame(master, background="#272727")
        execute_label = tk.Label(frame2, text="Execute section", font=('Arial', 10))
        execute_label.pack(pady=10)
        self.x_textbox = tk.Text(frame2, height=15, width=120, font=('Arial', 10))
        self.x_textbox.pack()

        frame2.pack(expand=True, fill="both", padx=10)

    def open_file(self):
        
        filetypes = (
            ('text files', '*.lol'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilenames(
            title='Open files',
            initialdir=os.getcwd(),
            filetypes=filetypes)

        # messagebox.showinfo(
        #     title='Selected Files',
        #     message=filename
        # )

        self.code_textbox.delete('1.0', "end")
        with open(str(filename)[2:-3], 'r') as a:
            self.code_textbox.insert("insert", a.read())

        # print(str(filename)[2:-3])
        pass

# class GUI:
#     def __init__(self):
#         self.root = tk.Tk()

#         self.menubar = tk.Menu(self.root)

#         self.filemenu = tk.Menu(self.menubar, tearoff=0)
#         self.filemenu.add_command(label="Open File", command=exit)

#         self.filemenu.add_separator()

#         self.menubar.add_cascade(menu=self.filemenu, label="File")

#         self.root.config(menu=self.menubar)



#         self.label = tk.Label(self.root, text="Some label", font=('Arial', 18))
#         self.label.pack(padx=10, pady=10)

#         self.tbox = tk.Text(self.root, height=5, font=('Arial', 18))
#         self.tbox.pack(padx=10, pady=10)

#         self.check_state = tk.IntVar()

#         self.check = tk.Checkbutton(self.root, text="Show mssg?", font=('Arial', 18), variable=self.check_state)
#         self.check.pack(padx=10, pady=10)

#         self.btn = tk.Button(self.root, text="click me", font=('Arial', 18), command=self.btnFunc)
#         self.btn.pack(padx=10, pady=10)

#         self.btn2 = tk.Button(self.root, text="exit", font=('Arial', 18), command=exit)
#         self.btn2.pack(padx=10, pady=10)

#         self.btn3 = tk.Button(self.root, text="clear", font=('Arial', 18), command=self.clear)
#         self.btn3.pack(padx=10, pady=10)

#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

#         self.root.mainloop()

#     def clear(self):
#         self.tbox.delete("1.0", tk.END)

#     def btnFunc(self):
#         if (self.check_state.get()):
#             messagebox.showinfo(title="txtbox info", message=self.tbox.get('1.0',  tk.END))
#             pass
#         else:
#             print(f"Check?: {self.tbox.get('1.0',  tk.END)[:-1]}")

#     def on_closing(self):
#         if messagebox.askyesno(title="U wanna leave me?", message="Do you really want to quit?"):
#             self.root.destroy()

GUI(root)

# root = tk.Tk()

# root.geometry("800x500")
# root.title("K Means Clustering")


# label = tk.Label(root, text="Hey", font=('Arial', 18))
# label.pack(padx=20, pady=20)

# textbox = tk.Text(root, height=3, font=('Arial', 16))
# textbox.pack(padx= 20, pady=20)

# entry = tk.Entry(root)
# entry.pack()

# button = tk.Button(root, text="Open file", font=('Arial', 16))
# button.pack(pady=20)

# frame1 = tk.Frame(root)
# frame1.columnconfigure(0, weight=1)
# frame1.columnconfigure(1, weight=1)
# frame1.columnconfigure(2, weight=1)

# btn1 = tk.Button(frame1, text="1", font=('Arial', 10))
# btn1.grid(row=0, column=0)

# btn2 = tk.Button(frame1, text="2", font=('Arial', 10))
# btn2.grid(row=2, column=0, sticky=tk.W+tk.E)

# frame1.pack(fill="x")


# hahabutton = tk.Button(root, text="haha", font=('Arial', 20))
# hahabutton.place(x= 400, y=400, height=50, width=50)

root.mainloop()




# # fonts
# font_1 = Font(family='Arial', 
#               size=24, 
#               weight='normal', 
#               slant='italic', 
#               underline=1, 
#               overstrike=1)

# font_2 = Font(family='Helvetica',
#               size=12,
#               weight='bold',
#               slant='italic',
#               underline=0,
#               overstrike=0)

# font_3 = Font(family='Courier', size=14, weight='normal', slant='roman', underline=0, overstrike=0)
# font_4 = Font(family='Times', size=22, weight='bold', slant='roman', underline=0, overstrike=0)



# references:
#   > open file in tkinter: https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/