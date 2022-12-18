from os import name
import os
import sys
from os.path import abspath, join
from pathlib import Path


SLASH = '\\' if name in ('nt', 'dos') else '/'
HOME = join(Path.home(),'user')

STUDENT_ROLE = 'student'


try:
    HOST = os.getenv('DB_HOST')
    PORT = int(os.getenv('DB_PORT'))

    if HOST == 'None':
        HOST = '192.168.0.174'#'192.168.223.1'
        print("Default host loaded")

    if PORT == 'None':
        PORT = 4001
        print("Default Port loaded")

except:
    HOST = '192.168.0.174'#'192.168.223.1'
    PORT = 4001#5000
    print("Error while retriving env vars")



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

