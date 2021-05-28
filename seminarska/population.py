import sys
from db import connect_db

c = connect_db()
cur = c.cursor()


# 2.g
def pop_obmocja(x, y, distance):
    cur.execute(
        "select sum(population) from naselje where x > {} and y > {} and x < {} and y < {}".format(x - distance,
                                                                                                   y - distance,
                                                                                                   x + distance,
                                                                                                   y + distance))
    result = cur.fetchone()
    return result[0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _, x, y, distance = sys.argv
        pop_obmocja(float(x), float(y), float(distance))
    else:
        print(pop_obmocja(40, 40, 10))
        print(pop_obmocja(40, 40, 20))
