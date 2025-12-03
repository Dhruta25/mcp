import random
import sqlite3
from fastmcp import FastMCP
import os
DB_PATH = os.path.join(os.path.dirname(__file__),"expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__),"categories.json")
mcp = FastMCP("Expense tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                  CREATE TABLE IF NOT EXISTS expenses(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL,
                  subcategory TEXT DEFAULT '',
                  note TEXT DEFAULT ''
                  )

        """)

init_db()

@mcp.tool()
def add_expenses(date,amount,category,subcategory="",note=""):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES (?,?,?,?,?)",
            (date,amount,category,subcategory,note)
        )
        return{'status':'ok','id':cur.lastrowid}
    
@mcp.tool()
def list_expense():
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT id,date,amount,category,subcategory,note FROM expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]
    
@mcp.tool()
def delete_expenses(id:int):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?",(id,))
        return {'status':'ok','rows_deleted':cur.rowcount}

@mcp.tool()
def expenses_range(start_date,end_date):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT id,date,amount,category,subcategory,note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC",
        (start_date,end_date))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]

@mcp.tool()
def update_expense(date,amount,category,subcategory="",note=""):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("UPDATE expenses SET amount=?, category=?, subcategory=?,notes=? WHERE date=?",
                        (amount,category,subcategory,note,date))
        return {"status":"ok"}

@mcp.tool()
def resources():
    with open(CATEGORIES_PATH,"r",encoding="utf-8",) as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport = "http",host = "0.0.0.0",port = 8000)
