import pyodbc

connection_string = (
    r'DRIVER={MySQL ODBC 8.0 ANSI Driver};'
    r'DATABASE=faks;'
    r'UID=root;'
    r'PWD=rootPass;'
    r'CHARSET=utf8mb4;'
)


def connect_db():
    c = pyodbc.connect(connection_string)
    c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    c.setencoding(encoding='utf-8')
    return c


def exec_ignore_duplicate(cur, sql):
    try:
        cur.execute(sql)
    except pyodbc.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            pass
        else:
            print("ERROR: " + str(e))
    except pyodbc.Error as e:
        print("ERROR: " + str(e))
