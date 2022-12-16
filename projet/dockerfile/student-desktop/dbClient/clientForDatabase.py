import socket
from ast import literal_eval as litteralEvaluation
from gestion import COMMIT, EXECUTE, EXECUTE_MANY, FETCHALL, FETCHONE, HOST, PORT



class databaseClient:
    def __init__(self, host, port, message='Connected') -> None:

        self.socket = socket.socket()
        self.__response__ = None
        print('[INFO] : Waiting for connection response...')
        self.socket.connect((host, port))
        print(f'[INFO] : {message}')

    def __enter__(self):
        return self


    def execute(self, sql, parameters):
        self.__callExecute__(EXECUTE, sql, parameters)


    def executemany(self, sql, parameters):
        self.__callExecute__(EXECUTE_MANY, sql, parameters)


    def fetchone(self):
        return self.__callExecute__(FETCHONE, None, None)


    def fetchall(self):
        return self.__callExecute__(FETCHALL, None, None)


    def commit(self):
        return self.__callExecute__(COMMIT, None, None)


    def __callExecute__(self, requestType, sql, parameters):
        try:
            encodedRequest = str((requestType, sql, parameters)).encode()
            self.socket.send(encodedRequest)

            encodedResponse = self.socket.recv(1024)
            DecodedResponse = litteralEvaluation(encodedResponse.decode())
            return DecodedResponse

        except ConnectionResetError:
            print('[ERROR] : Server connexion closed bye the remote host.')


    def close(self):
        self.__del__()


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass # Will call __del__


    def __del__(self):
        print('[INFO] : Client connection to SQL database closed')
        self.socket.close()



def ping():

    with databaseClient(HOST, PORT) as databaseConnection:
        print('pinged!')



def main():
    ping()

    # hash = '62cefe04ea3ed48f7941e7e02915adf23a4490d6396ebab88eee605fbb1ac96c'
    # username = 'Chris'
    # role = 'student'

    # with databaseClient(HOST, PORT) as databaseConnection:
    #     sql = """SELECT id FROM users WHERE username = ? and role = ?"""
    #     parameters = (username, role)

    #     databaseConnection.execute(sql, parameters)
    #     result = databaseConnection.fetchone()[0]
    #     print(result)

    #     sql = """SELECT * FROM files WHERE user_id = ?"""
    #     parameters = (result,)

    #     databaseConnection.execute(sql, parameters)
    #     print(databaseConnection.fetchall())


if __name__ == "__main__":
    main()
