from pyrqlite import dbapi2 as dbapi

from gestion import HOST, PORT, SLASH

from tabulate import tabulate





def read_tables(dbConnection):

    

    

    with dbConnection.cursor() as dbCursor:



        dbCursor.execute('SELECT name from sqlite_master where type="table"')



        tables = [ table[0] for table in dbCursor.fetchall() ]



        for table in tables:



            content = dbCursor.execute(f"SELECT * FROM {table}").fetchall()



            if table == 'users':

                header = ('id', 'role', 'username', 'password_hash')

                for row in range(len(content)):

                    content[row] = list(content[row])



            elif table == 'files':

                header = ('id', 'user_id', 'path', 'blob', 'hash')

                for row in range(len(content)):

                    content[row] = list(content[row])

                    content[row][2] = SLASH + content[row][2]

                    content[row][3] = repr(content[row][3])

                    

            print(table.upper()); print(tabulate(content, header, tablefmt='pretty'),'\n')



        



def main():

    

    dbConnection = dbapi.connect(host=HOST, port=PORT)



    try:

        read_tables(dbConnection)



    except Exception as error:

        print("[ERROR] : SQL connection failed, the database couldn't be printed:", error)



    finally:

        dbConnection.close()





if __name__ == "__main__":

    main()