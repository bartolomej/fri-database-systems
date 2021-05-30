from db import connect_db, exec_ignore_duplicate

c = connect_db()


# 4. naloga
def init_tables():
    cur = c.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS gostota_populacije ("
                "oid INTEGER PRIMARY KEY, "
                "density NUMERIC)")
    cur.execute("CREATE TABLE IF NOT EXISTS gostota_plemena ("
                "oid INTEGER, "
                "density NUMERIC,"
                "tid INTEGER,"
                "PRIMARY KEY (oid, tid),"
                "FOREIGN KEY (tid) REFERENCES pleme(tid))")


# igralno polje obsega (x,y) koordinate od (-400,-400) do (400,400)
def calculate_population_density(tribe_name=None):
    cur = c.cursor()
    step = 20
    oid = 0
    tid = None
    if tribe_name:
        cur.execute("SELECT tid FROM pleme WHERE tribe = '{}'".format(tribe_name))
        tid_res = cur.fetchone()
        tid = tid_res[0]
    for x in range(-400, 400 - step, step):
        oid += 1
        for y in range(-400, 400 - step, step):
            loc_cond = "x between {} and {} and y between {} and {}".format(x, x + step, y, y + step)
            if tribe_name:
                cur.execute(
                    "SELECT SUM(res.population) FROM "
                    "(SELECT DISTINCT vid, population FROM naselje n "
                    "inner join pleme p join igralec i on i.pid = n.pid where i.tid = {} and {}) as res".format(
                        tid, loc_cond))
            else:
                cur.execute(
                    "SELECT SUM(res.population) FROM "
                    "(SELECT DISTINCT vid, population FROM naselje n "
                    "inner join pleme p join igralec i on i.pid = n.pid where {}) as res".format(
                        loc_cond))
            density = cur.fetchone()[0]
            if density:
                if tribe_name:
                    exec_ignore_duplicate(cur,
                                          "INSERT INTO gostota_plemena VALUES ({}, {}, {})".format(oid, density / 100,
                                                                                                   tid))
                else:
                    exec_ignore_duplicate(cur,
                                          "INSERT INTO gostota_populacije VALUES ({}, {})".format(oid, density / 100))
            cur.commit()


if __name__ == '__main__':
    init_tables()
    calculate_population_density()
    calculate_population_density('Rimljani')
    calculate_population_density('Tevtoni')
    calculate_population_density('Galci')
    calculate_population_density('Natarji')
    calculate_population_density('Huni')
    calculate_population_density('Egipcani')
