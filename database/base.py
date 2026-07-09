
from database.neon import PostgresDB

class Persistance:
    def __init__(self):
        self.db = PostgresDB()
        
    def insert(self,tabel:str,data :dict):
        self.db.insert(tabel , data)
        print("INSERT Sucessfully ")
        
    def get_all(self,table:str = "useres"):
        data = self.db.get_all(table)
        # print(data)
        return data