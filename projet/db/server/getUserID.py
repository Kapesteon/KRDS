from pyrqlite import dbapi2 as dbapi
from sys import argv



def getUserID(host, port, username, passwordHash):
    '''Check if user is in database. If so, check if the hashsof both password match. If so return (True, user_id), else (False, None)'''

    dbConnection = dbapi.connect(host=host, port=port)

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
        raise Exception('BAD IP OR PORT')
    host = argv[1]
    port = argv[2]
    username = argv[3]
    passwordHash = argv[4]
    
    getUserID(host, port, username, passwordHash)


    return



if __name__ == "__main__":
    main()
