  
import tkinter as tk
from tkinter import ttk
 
 
# class Table:
     
#     def __init__(self,root):
         
#         # code for creating table
#         for i in range(total_rows):
#             for j in range(total_columns):
                 
#                 self.e = Entry(root, width=10, fg='black',
#                                font=('Arial',16,'bold'))
                 
#                 self.e.grid(row=i, column=j)
#                 self.e.insert(END, lst[i][j])
 
# # take the data
# lst = [(1,'Raj','Mumbai',19),
#        (2,'Aaryan','Pune',18),
#        (3,'Vaisasdadsadadhnavi','Mumbai',20),
#        (4,'Rachna','Mumbai',21),
#        (5,'Shubham','Delhi',21)]
  
# # find total number of rows and
# # columns in list
# total_rows = len(lst)
# total_columns = len(lst[0])
  
# # create root window
root = tk.Tk()
# t = Table(root)



# table : https://www.geeksforgeeks.org/create-table-using-tkinter/

contact_information = [['Code asdaadsadsadDelimiter OPEN', 'HAI'], 
['NEWLINE', '\\n'], 
['Variable Declaration', 'I HAS A'], 
['Variable Identifier', 'counter']]

columns = ('type', 'lexemes')

tree = ttk.Treeview(root, columns=columns, show='headings', style="mystyle.Treeview")

# define headings
tree.heading('type', text='Types')
tree.heading('lexemes', text='Lexemes')

# add data to the treeview
for contact in contact_information:
    # print(contact)
    tree.insert('', tk.END, values=contact)

tree.grid(row=0, column=0, sticky='nsew')

root.mainloop()
