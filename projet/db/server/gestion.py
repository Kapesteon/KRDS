from pathlib import Path
import sys
from os import name
from os.path import join
from tabulate import tabulate



HOME = Path(__file__).parent.resolve()
DATABASE = join(HOME,'app.db')
SLASH = '\\' if name in ('nt', 'dos') else '/'

HOST = '127.0.0.1'#'192.168.223.1'
PORT = 4001#5000

STUDENT_ROLE = 'student'

if len(sys.argv) == 1:
    print("No argument given")
    print("Localhost and default port loaded")

if len(sys.argv) == 2:
    print("1 argument given")
    HOST = sys.argv[1]

if len(sys.argv) >= 3:
    print("2 arguments given")
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])


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

    print(f'[{message}]')
    print(tabulate(
        [[tabulate(truncate(localFiles),    SUB_HEADER, tablefmt='simple'),
          tabulate(truncate(databaseFiles), SUB_HEADER, tablefmt='simple')]],
        HEADER, tablefmt='pretty'),'\n')
