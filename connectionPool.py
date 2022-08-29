# Object Pool pattern:
# Object Pool pattern is  to reduce the cost of establishing database connections.

import mysql.connector

class Connection():
    def __init__(self):
        self.cnxn = mysql.connector.connect(
            host="db4free.net",
            user="shn2002",
            passwd="shn20022002",
            database="shn2002"
        )

        self.cursor = self.cnxn.cursor()

    def __del__(self):
        self.cnxn.close()


class ConnectionPool:
    def __init__(self):
        self.__connections = [Connection()]

    def get_connection(self):
        return self.__connections.pop()

    def release_connection(self, connection):
        self.__connections.append(connection)


