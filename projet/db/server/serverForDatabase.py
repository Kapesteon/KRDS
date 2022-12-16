import sqlite3 as sqlite
import socket
import threading
import traceback
from ast import literal_eval as literalEvaluation
from gestion import COMMIT, DATABASE, EXECUTE, EXECUTE_MANY, FETCHALL, FETCHONE, HOST, PORT



def getLenghtRange(inputList):
    return range(len(inputList))



def connectToDatabase(database, message = 'Connected to SQLite database.'):
    connection = sqlite.connect(database)
    print(f'[INFO] : {message}')
    return connection, connection.cursor()



def clearDeadThreads(threadList):
    deletedThreads = 0
    for threadNumber in getLenghtRange(threadList):

        realThreadNumber = threadNumber - deletedThreads

        if not threadList[realThreadNumber].is_alive():
            threadList.pop(realThreadNumber)
            deletedThreads += 1



def multiThreadedClient(clientConnection, threadToJoin = None):
    if threadToJoin is not None:
        threadToJoin.join()
    try:
        with clientConnection:
            
            sqliteConnection, sqliteCursor = connectToDatabase(DATABASE, 'Connected to SQLite from threadServer!')

            with sqliteConnection:
                # clientConnection.send(str.encode('Connection established:'))

                while True:
                    data = clientConnection.recv(2048)
                    if not data: break
                    
                    requestType, sql, parameters = literalEvaluation(data.decode())
                    response = None

                    if requestType == EXECUTE: 
                        sqliteCursor.execute(sql, parameters)
                        response = True

                    elif requestType == EXECUTE_MANY: 
                        sqliteCursor.executemany(sql, parameters)
                        response = True

                    elif requestType == FETCHONE:
                        response = sqliteCursor.fetchone()

                    elif requestType == FETCHALL:
                        response = sqliteCursor.fetchall()

                    elif requestType == COMMIT:
                        sqliteConnection.commit()
                        response = True
                    else:
                        raise Exception('Wrong requestType!')

                    clientConnection.sendall(str(response).encode())

    except Exception as e:
        traceback.print_exc()
        print(e)
        exit(1)

 

def main():

    clientThreads = []


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSideSocket:
        serverSideSocket.bind((HOST, PORT))
        serverSideSocket.listen(5)
        print('[INFO] : Socket is listening..')

        try:
            while True:
                client, address = serverSideSocket.accept()
                print('[NEW CLIENT] : Connected to: ' + address[0] + ':' + str(address[1]))

                clearDeadThreads(clientThreads)
                threadToJoin = clientThreads[-1] if len(clientThreads) else None

                thread = threading.Thread(target=multiThreadedClient, args=(client, threadToJoin))
                clientThreads.append(thread)
                thread.start()
                print('[INFO] : Connected clients:',len(clientThreads))

        except KeyboardInterrupt:
            print('[INFO] : Ctrl-c was pressed, server closing.')
            serverSideSocket.close()

                

if __name__ == "__main__":
    main()