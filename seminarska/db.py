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