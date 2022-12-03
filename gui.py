from tkinter import ttk
import lexical_analyzer
import syntactic_analyzer
import semantic_analyzer

import os
import tkinter as tk
from tkinter import Entry, Frame, OptionMenu, Scrollbar, StringVar, messagebox
from tkinter import filedialog as fd
from tkinter.font import Font
from tkinter import scrolledtext
import textwrap

class GUI:
    def __init__(self):
        pass


root = tk.Tk()

lexemes = None
parse_tree = None
symbol_table = None


class GUI:
    def __init__(self, master):
        master.geometry("1300x700")
        master.resizable(False, False)

        frame1 = Frame(master, background="#272727")

        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)

        # ===================== lol code frame ==========================
        lolcode_frame = Frame(frame1, background="#272727")
        berlin_sans = Font(family='Berlin Sans', size=12, weight='bold')
        btn2 = tk.Button(lolcode_frame, text="Upload LOL code file", font=berlin_sans, width = 43, command=self.open_file)
        btn2.pack(pady=(10, 5), padx=(9, 15), fill="both")

        # Add a Scrollbar
        h=Scrollbar(lolcode_frame, orient='horizontal')
        h.pack(side=tk.BOTTOM, fill='both', padx=(9,15), pady=(0, 10))
        v=Scrollbar(lolcode_frame, orient='vertical')
        v.pack(side=tk.RIGHT, fill='both', padx=(0,15),)

        consolas_font = Font(family='Calibri', size=10, weight='normal') # TODO: not working
        self.code_textbox = tk.Text(lolcode_frame, height=20, width=60, font=consolas_font, bg="#DADADA", wrap="none", xscrollcommand=h.set, yscrollcommand=v.set)

        # Attach the scrollbar with the text widget
        h.config(command=self.code_textbox.xview)
        v.config(command=self.code_textbox.yview)

        self.code_textbox.pack(padx=10, pady=(0, 10), fill="both")

        lolcode_frame.grid(row=0, column=0, sticky="nsew")

        # ===================== lexemes frame ==========================
        lexemes_frame = Frame(frame1, background="#272727")
        lexemes_frame.grid(row=0, column=1, sticky="nsw")

        # -- using treeview for table --
        lextable_frame = Frame(lexemes_frame, background="#272727")
        columns = ('type', 'lexemes')

        c=Scrollbar(lexemes_frame, orient='vertical')
        c.pack(side=tk.RIGHT, fill='both', pady=(14, 20))

        # define headings
        self.style = ttk.Style()
        self.style.theme_use("clam") # clam, alt, 
        self.style.configure("Treeview",
            background = "silver",
            foreground = "black",
            rowheight = 23,
            fieldbackground = "white",
            )
        self.style.configure("Treeview.Heading", font=berlin_sans)
        self.style.map("Treeview",
            background = [("selected", "black")],
            foreground = [("selected", "white")])

        self.tree = ttk.Treeview(lextable_frame, columns=columns, show='headings', height=14, yscrollcommand=c.set)
        self.tree.heading('type', text='Type')
        self.tree.heading('lexemes', text='Lexeme')
        self.tree.grid(row=0, column=0, sticky='nsew', pady=10)
        self.tree.column("#1", stretch="yes", width=150)
        self.tree.pack(pady=(12,0))

        lextable_frame.pack()

        c.config(command=self.tree.yview)
        # -- using treeview for table --


        ''' attempt for better table to scroll colomn horizontally
        # table headers
        self.e = Entry(self.table_frame, width=15, justify='center', 
            font=berlin_sans, disabledforeground="black", disabledbackground="#b2b2b2")
        self.e.grid(row=0, column=0)
        self.e.insert(tk.END, "Type")
        self.e.configure(state="disabled")
        self.e = Entry(self.table_frame, width=22, justify='center',
            font=berlin_sans, disabledforeground="black", disabledbackground="#b2b2b2")
        self.e.grid(row=0, column=1)
        self.e.insert(tk.END, "Lexeme")
        self.e.configure(state="disabled")

        self.table_frame.pack(pady=(15,0), fill=None, expand=False)
        lexemes_frame.pack_propagate(False)
        '''
        # ===================== symbol table frame ==========================
        symbol_table_frame = Frame(frame1, background="#272727")
        symbol_table_frame.grid(row=0, column=2, sticky="nsw")


        # # -- using treeview for table --
        symboltable_frame = Frame(symbol_table_frame, background="#272727")
        columns = ('name', 'value', "type")

        c1=Scrollbar(symbol_table_frame, orient='vertical')
        c1.pack(side=tk.RIGHT, fill='both', pady=(14, 20))

        # define headings
        self.style = ttk.Style()
        self.style.theme_use("clam") # clam, alt, 
        self.style.configure("Treeview",
            background = "silver",
            foreground = "black",
            rowheight = 23,
            fieldbackground = "white",
            )
        self.style.configure("Treeview.Heading", font=berlin_sans)
        self.style.map("Treeview",
            background = [("selected", "black")],
            foreground = [("selected", "white")])

        self.tree_s = ttk.Treeview(symboltable_frame, columns=columns, show='headings', height=14, yscrollcommand=c1.set)
        self.tree_s.heading('name', text='Name')
        self.tree_s.heading('value', text='Value')
        self.tree_s.heading('type', text='Type')
        self.tree_s.grid(row=0, column=0, sticky='nsew', pady=10)
        # self.tree_s.column("#0", stretch="yes", width=90)
        self.tree_s.column('name', stretch="yes", width=100)
        self.tree_s.column('type', stretch="yes", width=90)
        self.tree_s.pack(pady=(12,0))

        symboltable_frame.pack()

        # self.symbol_table_textbox = tk.Text(symbol_table_frame, height=20, width=40, font=('Arial', 10))
        # self.symbol_table_textbox.pack(padx=10, pady=10)

        frame1.pack(expand=True, fill="both", padx=10, pady=10)

        # ===================== execute frame ==========================
        frame2 = Frame(master, background="#272727")
        execute_label = tk.Label(frame2, text="Execute section", font=('Arial', 10))
        execute_label.pack(pady=10)
        self.x_textbox = tk.Text(frame2, height=15, width=120, font=('Arial', 10))
        self.x_textbox.pack()

        frame2.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    def open_file(self):
        
        filetypes = (
            ('text files', '*.lol'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilenames(
            title='Open files',
            initialdir=os.getcwd(),
            filetypes=filetypes)

        filename = str(filename)[2:-3] # removing parenthesis and apostrophes

        self.code_textbox.delete('1.0', "end")
        with open(filename, 'r') as a:
            self.code_textbox.insert("insert", a.read())

        global lexemes, parse_tree, symbol_table
        lexemes = lexical_analyzer.lex_main(filename)
        self.show_lexemes()

        parse_tree = syntactic_analyzer.syntax_main(lexemes)
        symbol_table = semantic_analyzer.semantic_main(parse_tree)
        self.show_symbol_table()
        print(symbol_table)


        # self.fill_lexeme_table() # fill the lexeme table 

    '''
    def fill_lexeme_table(self):
        global lexemes
        total_rows = len(lexemes)
        total_columns = len(lexemes[1])
        print(f"row: {total_rows} == col: {total_columns}")
        for i in range(total_rows):
            for j in range(total_columns):
                 
                self.e = Entry(self.table_frame, width=15 if j==0 else 22,
                    font=('Berlin Sans',11,'normal'), disabledforeground="black")
                 
                self.e.grid(row=i+1, column=j)
                self.e.insert(tk.END, lexemes[i][j])
                self.e.configure(state='disabled')
        # berlin_sans = Font(family='Berlin Sans', size=12, weight='bold')
        # self.e = Entry(self.table_frame, width=15, justify='center', 
        #     font=berlin_sans, disabledforeground="black", disabledbackground="#b2b2b2")
        # self.e.grid(row=1, column=0)
        # self.e.insert(tk.END, "Type")
        # self.e.configure(state="disabled")

        # self.e = Entry(self.table_frame, width=15, justify='center', 
        #     font=berlin_sans, disabledforeground="black", disabledbackground="#b2b2b2")
        # self.e.grid(row=1, column=1)
        # self.e.insert(tk.END, "Type")
        # self.e.configure(state="disabled")
    '''

    # function for treeview
    def show_lexemes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        global lexemes
        if (isinstance(lexemes[0], str)):
            error = lexemes.pop(0)
            lexemes.append(["ERROR:", error[7:]])
        for lexeme in lexemes:
            self.tree.insert('', tk.END, values=lexeme)

    def show_symbol_table(self):
        for item in self.tree_s.get_children():
            self.tree_s.delete(item)

        global symbol_table
        for val in symbol_table:
            self.tree_s.insert('', tk.END, values=val)

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

root.mainloop()


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
#   > color picker: https://imagecolorpicker.com/color-code
#   > table tkinter: https://www.youtube.com/watch?v=ewxT3ZEGKAA

