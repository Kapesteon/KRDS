# from gestion import DATABASE
from hashlib import sha256
from pyrqlite import dbapi2 as dbapi
from traceback import print_exc
from printDatabase import read_tables
from sys import argv


def create_tables(connection):
    
    with connection.cursor() as cursor:

        if len(argv) == 4 and argv[3]:
            if argv[3] == 'reset':
                print('[INFO] The database has been reset')
                cursor.execute('DROP TABLE IF EXISTS files')
                cursor.execute('DROP TABLE IF EXISTS users')
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            integer PRIMARY KEY,
                role          text NOT NULL,
                username      text NOT NULL,
                password_hash text NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id      integer NOT NULL,
                user_id integer NOT NULL,
                path    text    NOT NULL,
                blob    text    NOT NULL,
                hash    text    NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (user_id) REFERENCES users (user_id) 
            );
        """)
    



def fill_user(connection):

    sql = 'INSERT INTO users (role, username, password_hash) values(?, ?, ?)'
    data = [
        ('student', 'Alice', sha256('Merveille'.encode()).hexdigest()),
        ('student', 'Bob',   sha256('Chapeau'.encode()).hexdigest()),
        ('student', 'Chris', sha256('Tof'.encode()).hexdigest()) ]

    with connection.cursor() as cursor:
        cursor.executemany(sql, data)





def main():

    connection = dbapi.connect(host=HOST, port=PORT,) # create if doesn't exist

    try:
        create_tables(connection)
        fill_user(connection)
        read_tables(connection)

    except Exception as error:
        print_exc()
        print("[ERROR] : SQL connection failed, the database couldn't be initialised:", error)

    finally:
        connection.close()

    return



if __name__ == "__main__":
    main()
