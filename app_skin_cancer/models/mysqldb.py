# class database
import mysql.connector
from models.config import settings

class MysqlConnect:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cnn = None        

    def connect(self):
        self.cnn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )

    def close(self):
        if self.cnn is not None:
            self.cnn.close()
    
    def execute_query(self, query, data = None):
        cursor = self.cnn.cursor()
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()

        return result
    
    def query_id(self, query):
        cursor = self.cnn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        return result

    def execute_sprocedure(self, sp_name, *args):
        try:
            cursor = self.cnn.cursor()
            cursor.callproc(sp_name, args)
            self.cnn.commit()
            result = 1
        except mysql.connector.Error as error:
            result = 0
            print(error)
        finally:
            cursor.close()

        return result

    def execute_procedure_query(self, sp_name, *args):
        cursor = self.cnn.cursor()
        cursor.callproc(sp_name, args)
        rows_data = []
        for result in cursor.stored_results():
            rows_data.extend(result.fetchall())
        cursor.close()

        return rows_data        

# settings for mysql connection
mysql_cnn = MysqlConnect(**settings)
