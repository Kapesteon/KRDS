from pyrqlite import dbapi2 as dbapi
from gestion import HOME, HOST, PORT, SLASH, exitError
from hashlib import sha256
from os import chdir, mkdir, remove, walk, getenv
from os.path import basename, exists, getsize, isdir, join
from pathlib import PurePath
# from shutil import rmtree
# from pathlib import Path



class FilesStatus:
    def __init__(self, moved=[], edited=[], created=[], deleted=[]):
        self.moved = moved
        self.edited = edited
        self.created = created
        self.deleted = deleted



# GET FILE HASH, COMPARE IT WITH THE ONE IN THE DB TO:
#   Know if it has been deleted
#     - Then also delete it from the db
#   Know if it has beed moved
#     - Then just change the file path in the db
#   Know if it has been created
#      -Then create it to add it in the db
def hashFile(filePath):
    '''Return hash of a file'''

    # An arbitrary buffer size of 64 kilobytes
    BUFFER_SIZE = 65536
    hash = sha256()

    with open(filePath, 'rb') as fileContent:
        while True:
            # Reading data by blocs of lenght BUG_SIZE
            filePart = fileContent.read(BUFFER_SIZE)

            if not filePart: break # Breaks when eof met
            hash.update(filePart)  # Update hash with new bloc

    # sha256.hexdigest() hashes all the input data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which all the input data gets hashed hexdigest()
    # hashes the data, and returns the output in hexadecimal format
    return hash.hexdigest()



def collectUserLocalFiles(pathWhereCollect):
    '''Return all the absolute path of the files under "pathWhereCollect"'''
    collection = [] 

    for root, directories, files in walk(pathWhereCollect):
        for file in files:

            filePath = str(PurePath(join(root, file)).relative_to(HOME))

            if (getsize(filePath)): # If size == 0 file is not appended
                collection.append((filePath, hashFile(filePath)))

    return collection



def getPathHashFromDatabase(databaseConnection, userID):
    '''Get all the user path/hash files from the database.'''

    sqlFetchFilesQuery = """SELECT path, hash from files where user_id = ?"""

    with databaseConnection.cursor() as databaseCursor:

        databaseCursor.execute(sqlFetchFilesQuery, (userID,))

        return databaseCursor.fetchall()



def convertIntoBinary(filePath):
    '''Get files as binnary value. To be send to the database.'''
    with open(filePath, 'rb') as file:
        binary = file.read()
    return binary



def setFlagFromLists(lists, element, flag, subelement=None):
    for list in lists:

        if subelement == None:
            list[list.index(element)] = flag

        else:
            for row in range(len(list)):
                if list[row][subelement] == element:
                    list[row] = flag
                    break



def clearFlagFromLists(lists, flag):
    return [ [ element for element in list if element != flag] for list in lists ]



def getPackedSortedFiles(userID, localFiles, databaseFiles):

    PATH_INDEX = 0
    HASH_INDEX = 1
    REMOVED_FILE = ('','')
    filesStatus = FilesStatus()

    # printDebugLocalDB(localFiles, databaseFiles, 'INIT')

    # Same files, nothing to do so remove them from list
    for localFile in localFiles:
        if localFile in databaseFiles:
            setFlagFromLists((databaseFiles, localFiles), localFile, REMOVED_FILE)

    localFiles, databaseFiles = clearFlagFromLists((localFiles, databaseFiles), REMOVED_FILE)
    # printDebugLocalDB(localFiles, databaseFiles, 'AFTER_SAME_FILES_REMOVED')


    # File edited (check if path maches but not hash)
    for localFile in localFiles:
            for databaseFile in databaseFiles:
                if localFile[PATH_INDEX] == databaseFile[PATH_INDEX] and localFile != REMOVED_FILE:

                    filePath, fileHash = localFile
                    fileBinary = convertIntoBinary(filePath)
                    filesStatus.edited.append([fileBinary, fileHash, userID, filePath])

                    setFlagFromLists((databaseFiles, localFiles), filePath, REMOVED_FILE, PATH_INDEX)
                    break
    
    localFiles, databaseFiles = clearFlagFromLists((localFiles, databaseFiles), REMOVED_FILE)   
    # printDebugLocalDB(localFiles, databaseFiles, 'AFTER_EDITED_FILES_REMOVED')

    # File moved (same hash but different path)
    for databaseFile in databaseFiles:
        for localFile in localFiles:
            if databaseFile[HASH_INDEX] == localFile[HASH_INDEX] and localFile != REMOVED_FILE:

                newFilePath, fileHash = localFile
                oldFilePath = databaseFile[PATH_INDEX]
                filesStatus.moved.append([newFilePath, userID, oldFilePath])

                setFlagFromLists((databaseFiles, localFiles), fileHash, REMOVED_FILE, HASH_INDEX)
                break

    localFiles, databaseFiles = clearFlagFromLists((localFiles, databaseFiles), REMOVED_FILE) 
    # printDebugLocalDB(localFiles, databaseFiles, 'AFTER_MOVED_FILES_REMOVED')

    # File created (not found in database)
    for localFile in localFiles:

        filePath, fileHash = localFile
        fileBinary = convertIntoBinary(filePath)

        filesStatus.created.append([userID, filePath, fileBinary, fileHash])

    # File deleted (not found in local HOME)
    for databaseFile in databaseFiles:
        filesStatus.deleted.append([userID, databaseFile[PATH_INDEX]])

    return filesStatus



def sendRequest(databaseConnection, request, data, message, fileNameIndex):
    
    with databaseConnection.cursor() as databaseCursor:
        databaseCursor.executemany(request, data)

    databaseConnection.commit()

    if len(data):
        print(f'[DATA] : {message} files {[basename(f[fileNameIndex]) for f in data]}')



# Prepare 4 requests to either:
#   1. Change path     (moved)
#   2. Change blob     (edited)
#   3. Insert new blob (created)
#   4. Delete blob     (deleted)
# Then upload (executemany())
def uploadUserFiles(databaseConnection, filesStatus): 
    '''Upload (after erasing) the user current personnal data to the database.'''

    # Prepare sqlite request
    sqlMovedFileQuery =   'UPDATE      files SET path = ?               WHERE user_id = ? and path = ?' # ? to prevent sqlite injection attacks
    sqlEditedFileQuery =  'UPDATE      files SET blob = ?, hash = ?     WHERE user_id = ? and path = ?'
    sqlCreatedFileQuery = 'INSERT INTO files(user_id, path, blob, hash) VALUES(?, ?, ?, ?)'
    sqlDeletedFileQuery = 'DELETE FROM files                            WHERE user_id = ? and path = ?'

    # Send requests
    sendRequest(databaseConnection, sqlMovedFileQuery,   filesStatus.moved,   'Moved',   0)
    sendRequest(databaseConnection, sqlEditedFileQuery,  filesStatus.edited,  'Edited',  3)
    sendRequest(databaseConnection, sqlCreatedFileQuery, filesStatus.created, 'Created', 1)
    sendRequest(databaseConnection, sqlDeletedFileQuery, filesStatus.deleted, 'Deleted', 1)


def cleanUp(home):
    # remove(Path(__file__).parent.resolve())
    return
    
    

# DISCONNECTION
def disconnect():
    '''Shouldn't be needed when user leave k8s container, but needed for dev purpose.'''

    if not isdir(HOME):
        return exitError('Home not found. The data haven\'t been uploaded and is lost.')

    chdir(HOME)
    
    userID = getenv('USERID')
    localFiles = collectUserLocalFiles(HOME) # List of tuple (path, hash)

    databaseConnection = dbapi.connect(HOST, PORT)

    try:
        databaseFiles = getPathHashFromDatabase(databaseConnection, userID)  # List of tuple (path, hash)
        filesStatus = getPackedSortedFiles(userID, localFiles, databaseFiles) # Class of four list of files (moved, edited, created, deleted)
        
        uploadUserFiles(databaseConnection, filesStatus)
    
    except Exception as error:
        print("[ERROR] : Failed to upload user files to sqlite database:", error)

    finally:
        databaseConnection.close()

    cleanUp(HOME)



def main():
    disconnect()
    return


# TODO: delete user
# TODO: One table by user
# TODO: One db file per user

if __name__ == "__main__":
    main()
