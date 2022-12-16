from gestion import HOST, PORT, exitError
from getpass import getpass
from hashlib import sha256
from pyrqlite import dbapi2 as dbapi



def hash(password):
    return sha256(password.encode()).hexdigest()



def getUserID(databaseConnection, username, passwordHash):
    '''check if user is in database. If so, check if the hash of both password match. If so return (True, user_id), else (False, None)'''

    databaseConnection.execute('SELECT id, password_hash FROM users WHERE username=?', (username,))
    requestResult = databaseConnection.fetchone()
    if requestResult == None: exitError('Account not found.')

    userID, fetchedHash = requestResult
    if fetchedHash != passwordHash: exitError('Login Fail.')

    print("[INFO] : Login Success.")
    return userID



def deleteUser(databaseConnection, userID):

    sqlDeleteUserFilesQuery = '''DELETE FROM files WHERE user_id = ?''' # ?,? to prevent sqlite injection attacks
    sqlDeleteUserFilesData = (userID,)
    sqlDeleteUserQuery = '''DELETE FROM users WHERE id = ?''' # ?,? to prevent sqlite injection attacks
    sqlDeleteUserData = (userID,)

    databaseConnection.execute(sqlDeleteUserFilesQuery, sqlDeleteUserFilesData)
    databaseConnection.execute(sqlDeleteUserQuery,      sqlDeleteUserData)
    databaseConnection.commit()


    print("[INFO] : The user", userID, "and their files have been deleted from the database.") 

    

def create_user():
    username = input('Username: ')
    password = getpass('Password: ')

    try:
        databaseConnection = dbapi.connect(HOST, PORT)

        # Get and save user ID
        userID = getUserID(databaseConnection, username, hash(password))

        deleteUser(databaseConnection, userID)
    
    except Exception as error:
        print("[ERROR] : SQL connection failed, the user has not been added to the database:", error)

    finally:
        databaseConnection.close()



def main():
    create_user()



if __name__ == "__main__":
    main()