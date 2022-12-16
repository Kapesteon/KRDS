from os import name
import sys
from os.path import abspath, join
from pathlib import Path


SLASH = '\\' if name in ('nt', 'dos') else '/'
HOME = Path.home()


SESSION_USER = join(HOME,f'..{SLASH}','.session.conf')
STUDENT_ROLE = 'student'


HOST = '127.0.0.1'#'192.168.223.1'
PORT = 65432#5000


EXECUTE = 'execute'
EXECUTE_MANY = 'executemany'
FETCHONE = 'fetchone'
FETCHALL = 'fetchall'
COMMIT = 'commit'



def returnError(message, objectToReturn=1):
    print(f'[Error] : {message}')
    return objectToReturn
    
    

def exitError(message, objectToReturn=1):
    print(f'[Error] : {message}')
    exit(objectToReturn)


"""
def printDebugLocalDB(localFiles, databaseFiles, message='INIT'):
    PATH_INDEX = 0
    HASH_INDEX = 1
    HEADER = ['LOCAL', 'DATABASE']
    SUB_HEADER = ['Path', 'Hash']

    def truncate(files):
        content = files.copy()
        for file in range(len(content)):
            content[file] = list(content[file])
            content[file][PATH_INDEX] = content[file][PATH_INDEX].split(HOME)[1]
            content[file][HASH_INDEX] = content[file][HASH_INDEX][-10:]
        return content
"""

