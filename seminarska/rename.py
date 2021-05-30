from db import connect_db

# Naloga 3.j

c = connect_db()

cur = c.cursor()


def rename():
    cur.execute(
        "select vid from igralec i inner join naselje n on i.pid = n.pid where i.player = 'Sirena' order by n.population desc");
    ordered_result = cur.fetchall()

    for index, res in enumerate(ordered_result):
        vid, = res
        cur.execute("update naselje set village = 'Grad {}' where vid = {}".format("{0:02}".format(index + 1), vid))
    cur.commit()


if __name__ == '__main__':
    rename()
