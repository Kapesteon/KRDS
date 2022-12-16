from gestion import HOST, PORT, STUDENT_ROLE
from hashlib import sha256
from getpass import getpass
from pyrqlite import dbapi2 as dbapi



def verifyUsername(databaseConnection, username):
    
    databaseConnection.execute('SELECT username FROM users WHERE username=?', (username, ))

    if databaseConnection.fetchone() is not None:
        print("[ERROR] Username already exists, please choose another one.")
        exit(1)



def verifyPassword(password, confirmation):
    if password != confirmation:
        print("[ERROR] Password doesn't match.")
        exit(1)



def hash(password):
    return sha256(password.encode()).hexdigest()



def addUser(databaseConnection, username, password):

    passwordHash = hash(password)
    sqlInsertUserData = (STUDENT_ROLE, username, passwordHash)
    sqlInsertUserQuery = '''INSERT INTO users(role, username, password_hash) VALUES(?, ?, ?)''' # ?,? to prevent sqlite injection attacks

    databaseConnection.execute(sqlInsertUserQuery, sqlInsertUserData)
    databaseConnection.commit()
    print("[INFO] : The user ", username, " has been added to the database.") 

    

def create_user():

    databaseConnection = dbapi.connect(HOST, PORT)

    try:

        username = input('Username: ')
        verifyUsername(databaseConnection, username)

        password = getpass('Password: ')
        passwordConfirmation = getpass('Confirm your password: ')
        verifyPassword(password, passwordConfirmation)

        addUser(databaseConnection, username, password)
    
    except Exception as error:
        print("[ERROR] : SQL connection failed, the user has not been added to the database:", error)

    finally:
        databaseConnection.close()



def main():
    create_user()



if __name__ == "__main__":
    main()