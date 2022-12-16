from db.client.clientForDatabase import databaseClient
from sys import argv
import traceback



def getUserID(host, port, username, passwordHash):
    '''Check if user is in database. If so, check if the hashsof both password match. If so return (True, user_id), else (False, None)'''

    try:
        databaseConnection = databaseClient(host, port, 'Connected to SQLite to open session.')
        databaseConnection.execute('SELECT id, role, password_hash FROM users WHERE username=?', (username,))

        requestResult = databaseConnection.fetchone()
        if requestResult == None: raise Exception('Account not found.')

        userID, userRole, fetchedHash = requestResult
        if fetchedHash != passwordHash: raise Exception('Login Fail.')

        print("[INFO] : Login Success.")

    except Exception as error:
        print("[ERROR] : SQL connection failed, the user files have not been download:", error)
        databaseConnection.close()
        return (-1,"")

    databaseConnection.close()
    return userID, userRole



def main():
    if len(argv) != 5:
        raise Exception('Walla \'faut mettre l\'IP et le port frero! Et oublie pas le mdp et le usr sinon ça marchera jamais')
    host = argv[1]
    port = argv[2]
    username = argv[3]
    passwordHash = argv[4]

    getUserID(host, port, username, passwordHash)
    return



if __name__ == "__main__":
    main()