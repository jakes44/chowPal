import sqlite3


def get_order_history(uid):
  db = sqlite3.connect('DB/chow.db')
  c = db.cursor()

  return c.execute("select did,rating from choices where uid=?",(uid,)).fetchall()


