r"""
    Creating GUI using tkinter default Python library
"""

from tkinter import *
import sqlite3

window=Tk()


def create_database():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todo(id INTEGER, todo TEXT, status INTEGER)")
    conn.commit()
    conn.close()


def add_todo():
    task = todoText.get() + "\n"
    viewPort.insert(END, task)

    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO todo VALUES (?,?,?)", (1, task, 0))
    conn.commit()
    conn.close()
    print("Todo added.")


def select_todo():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_todo(task, item_idx):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("UPDATE todo SET todo=? WHERE id=?", (task, item_idx))
    conn.commit()
    conn.close()


def delete_all_todo():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM todo")
    conn.commit()
    conn.close()
    viewPort.delete(1.0, END)


def delete_todo(item_idx):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE id=?", (item_idx,))
    conn.commit()
    conn.close()
    viewPort.delete(1.0, END)


def get_all_todo():
    # clearing the view port text field
    viewPort.delete(1.0, END)
    rows = select_todo()  # selecting all todos from the database
    for row in rows:
        viewPort.insert(END, row)


# Input TODOs
todoText = StringVar()
todo=Entry(window, textvariable=todoText)
todo.grid(row=0,column=0)
# The View port to show todos
viewPort = Text(window, height=5, width=50)
viewPort.grid(row=1, column=0)
# Add button
btnAdd = Button(window, text="Add", command=add_todo)
btnAdd.grid(row=0,column=4)
# Edit button
btnEdit = Button(window, text="Edit", command=add_todo)
btnEdit.grid(row=1,column=4)
# View button
btnView = Button(window, text="View", command=add_todo)
btnView.grid(row=3,column=4)
# Delete button
btnDelete = Button(window, text="Delete", command=delete_todo)
btnDelete.grid(row=2,column=4)
# Delete all button
btnDeleteAll = Button(window, text="Delete", command=delete_all_todo)
btnDeleteAll.grid(row=2,column=4)

# Creating database
create_database()
get_all_todo()

window.mainloop()
