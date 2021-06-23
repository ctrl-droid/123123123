import pymysql

class memVo:
    def __init__(self, id=None, pwd=None, name=None, tel=None, point=0):
        self.id = id
        self.pwd = pwd
        self.name = name
        self.tel = tel
        self.point = point

    def __str__(self):
        return 'id:'+self.id+' / pwd:'+self.pwd+' / name:'+self.name+' / tel:'+self.tel+' / point:'+str(self.point)



class memDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='movie_reserve', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into member values(%s, %s, %s, %s, %s)"
        vals = (vo.id, vo.pwd, vo.name, vo.tel, vo.point)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def
