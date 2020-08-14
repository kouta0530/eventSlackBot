import psycopg2
import psycopg2.extras

class PosDB:
    def __init__(self,host,dbname,user,password,port):
        self.conn = psycopg2.connect(host = host,dbname = dbname,user = user,password = password,port = port)

    def set_cursor(self):
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    def command(self,command): 
        self.cur.execute(command)
        res = self.cur.fetchall()
        
        dict_result = []
        for row in res:
            dict_result.append(dict(row))
        
        return dict_result


    


