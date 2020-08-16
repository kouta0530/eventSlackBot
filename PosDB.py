import psycopg2
import psycopg2.extras

class PosDB:
    def __init__(self,url):
        self.conn = psycopg2.connect(url)

    def set_cursor(self):
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    def select_command(self,command): 
        self.cur.execute(command)
        res = self.cur.fetchall()
        
        dict_result = []
        for row in res:
            dict_result.append(dict(row))
        return dict_result

    def insert_command(self,command): 
        self.cur.execute(command)
        self.conn.commit()
        return 0

    def close(self):
        self.cur.close()
        self.conn.close()
    

