from gestion import HOST, PORT
from pyrqlite import dbapi2 as dbapi
from sys import argv



def getUserID(port, host, username, passwordHash):
    '''Check if user is in database. If so, check if the hashsof both password match. If so return (True, user_id), else (False, None)'''

    dbConnection = dbapi.connect(host=HOST, port=PORT)

    try:

        with dbConnection.cursor() as dbCursor:

            dbCursor.execute('SELECT id, role, password_hash FROM users WHERE username=?', (username,))

            requestResult = dbCursor.fetchone()
            if requestResult == None: raise Exception('Account not found.')

            userID, userRole, fetchedHash = requestResult
            if fetchedHash != passwordHash: raise Exception('Login Fail.')

            print("[INFO] : Login Success.")

    except Exception as error:
        print("[ERROR] : SQL connection failed, the user files have not been download:", error)
        dbConnection.close()
        return (-1,"")

    dbConnection.close()
    return userID, userRole
    



def main():

    if len(argv) != 5:
        raise Exception('Walla \'faut mettre l\'IP et le port frero! Et oublie pas le mdp et le usr sinon ça marchera jamais')
        
    username = argv[3]
    passwordHash = argv[4]
    
    getUserID(None, None, username, passwordHash)


    return



if __name__ == "__main__":
    main()