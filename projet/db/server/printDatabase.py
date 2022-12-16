import sqlite3 as sqlite
from gestion import DATABASE, SLASH, exitError
from os.path import exists
from tabulate import tabulate


def read_tables():
    if not exists(DATABASE):
        exitError('Database not found.')
    connection = sqlite.connect(DATABASE)
    with connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name from sqlite_master where type="table"')
        tables = [ table[0] for table in cursor.fetchall() ]
        for table in tables:

            content = connection.execute(f"SELECT * FROM {table}").fetchall()

            if table == 'users':
                header = ('id', 'role', 'username', 'password_hash')
            elif table == 'files':
                header = ('id', 'user_id', 'path', 'blob', 'hash')
                for row in range(len(content)):
                    content[row] = list(content[row])
                    content[row][2] = SLASH + content[row][2]
                    content[row][3] = repr(content[row][3])
                    
            print(table.upper()); print(tabulate(content, header, tablefmt='pretty'),'\n')

        
def main():
    read_tables()
    return


if __name__ == "__main__":
    main()