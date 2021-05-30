import pyodbc
from db import connect_db, exec_ignore_duplicate

c = connect_db()

cur1 = c.cursor()
cur2 = c.cursor()

cur1.execute("CREATE TABLE IF NOT EXISTS pleme ("
             "tid INTEGER PRIMARY KEY, "
             "tribe VARCHAR(30))")

cur1.execute("CREATE TABLE IF NOT EXISTS aliansa ("
             "aid INTEGER PRIMARY KEY, "
             "alliance VARCHAR(30))")

cur1.execute("CREATE TABLE IF NOT EXISTS igralec ("
             "pid INTEGER PRIMARY KEY, "
             "player VARCHAR(30), "
             "tid INTEGER, "
             "aid INTEGER,"
             "FOREIGN KEY (tid) REFERENCES pleme(tid),"
             "FOREIGN KEY (aid) REFERENCES aliansa(aid))")

cur1.execute("CREATE TABLE IF NOT EXISTS naselje ("
             "vid INTEGER PRIMARY KEY,"
             "village VARCHAR(30),"
             "x INTEGER NOT NULL,"
             "y INTEGER NOT NULL,"
             "population INTEGER,"
             "pid INTEGER,"
             "FOREIGN KEY (pid) REFERENCES igralec(pid),"
             "CONSTRAINT x CHECK (x >= -250 AND x <= 250),"
             "CONSTRAINT y CHECK (y >= -250 AND y <= 250))")
c.commit()

cur2.execute("SELECT * FROM x_world")
rows = cur2.fetchall()

id_plemena_map = {
    1: "Rimljani",
    2: "Tevtoni",
    3: "Galci",
    4: "Narava",
    5: "Natarji",
    6: "Huni",
    7: "Egipcani"
}

for tid in id_plemena_map:
    exec_ignore_duplicate(cur2, "INSERT INTO pleme VALUES ({}, '{}')".format(tid, id_plemena_map[tid]))

for row in rows:
    _, x, y, tid, vid, village, pid, player, aid, alliance, population = row
    exec_ignore_duplicate(cur2, "INSERT INTO aliansa VALUES ({}, '{}')".format(aid, alliance))
    exec_ignore_duplicate(cur2, "INSERT INTO igralec VALUES ({}, '{}', {}, {})".format(pid, player, tid, aid))
    exec_ignore_duplicate(cur2, "INSERT INTO naselje VALUES ({}, '{}', {}, {}, {}, {})".format(vid, village, x, y, population, pid))

cur2.execute("UPDATE igralec SET aid = null WHERE aid = 0;")
cur2.execute("DELETE FROM aliansa WHERE aid = 0")

cur2.commit()

c.close()
