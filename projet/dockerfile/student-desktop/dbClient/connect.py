from pyrqlite import dbapi2 as dbapi
from gestion import HOME, HOST, PORT, exitError, returnError
from hashlib import sha256
from os import makedirs, getenv#, remove
from os.path import basename, dirname, join



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




def getUserDatabaseFiles(databaseConnection, userID):
    '''Get all the user files from the database.'''

    with databaseConnection.cursor as databaseCursor:

        sqlFetchBlobQuery = """SELECT path, blob FROM files WHERE user_id = ?"""

        databaseCursor.execute(sqlFetchBlobQuery, (userID,))
        userDatabaseFiles = databaseCursor.fetchall()
        
        if userDatabaseFiles == []:
            print('[INFO] : Nothing retrieved.')
            exit(0)

    return userDatabaseFiles



def writeToFile(filePath, binaryFile):
    '''Create path if doesn't exist and write file'''
    absPath = join(HOME, filePath)
    makedirs(dirname(absPath), exist_ok=True)

    with open(absPath, 'wb') as file:
        try: 
            file.write(binaryFile)
        except: 
            returnError(f'TypeError: a bytes-like object is required, not "str". binaryFile: ${binaryFile}')

    print("[DATA] : The following file has been written:", basename(absPath))



def writeUserDatabaseFiles(userDatabaseFiles):
    '''Retrieve user personnal data from the db and add them on the user session'''
    for row in userDatabaseFiles:
        filePath, photoBinarycode = row
        writeToFile(filePath, photoBinarycode)

    print(f"[INFO] : Data successfully stored on disk. Check {HOME}.")
    return
        


def connect():

    databaseConnection = dbapi.connect(HOST, PORT)

    try:
        # Get and save user ID
        userID = int(getenv('USERID'))
        
        # Download user files
        userDatabaseFiles = getUserDatabaseFiles(databaseConnection, userID)
        writeUserDatabaseFiles(userDatabaseFiles)
    
    except Exception as error:
        print("[ERROR] : SQL connection failed, the user files have not been download:", error)

    finally:
        databaseConnection.close()



def main():
    connect()
    # remove(__file__)
    return



if __name__ == "__main__":
    main()