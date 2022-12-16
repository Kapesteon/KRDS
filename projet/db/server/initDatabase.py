from gestion import DATABASE
from hashlib import sha256
from serverForDatabase import sqlite



def create_tables():
    connection = sqlite.connect(DATABASE) # create if doesn't exist
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            integer PRIMARY KEY,
                role          text NOT NULL,
                username      text NOT NULL,
                password_hash text NOT NULL
            );
        """)
        connection.execute("""
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



def fill_user():
    connection = sqlite.connect(DATABASE)

    sql = 'INSERT INTO users (role, username, password_hash) values(?, ?, ?)'
    data = [
        ('student', 'Alice', sha256('Merveille'.encode()).hexdigest()),
        ('student', 'Bob',   sha256('Chapeau'.encode()).hexdigest()),
        ('student', 'Chris', sha256('Tof'.encode()).hexdigest()) ]

    with connection:
        connection.executemany(sql, data)



def main():
    create_tables()
    fill_user()
    return



if __name__ == "__main__":
    main()