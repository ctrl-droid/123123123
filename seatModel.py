import pymysql
import movie_reserve.theaterModel as thm

'''
code	int
name	varchar(45)
price	int
available	tinyint
theater_code	int
'''

class seatVo:
    def __init__(self, code=0, name=None, price=0, available=False, theater_code=0):
        self.code = code
        self.name = name
        self.price = price
        self.available = available
        self.theater_code = theater_code

    def __str__(self):
        return '좌석이름:' + self.name + ' / 가격:' + str(self.price) + ' / 좌석선점:' + str(self.available)

class seatDao:
    def __init__(self):
        self.conn = None

    # db연결함수
    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='movie_reserve', charset='utf8')

    # db 닫는 함수
    def disconnet(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into seat(name, price, available, theater_code) values(%s, %s, %s, %s)"
        vals = (vo.name, vo.price, vo.available, vo.theater_code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def select(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from seat where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnet()
        if row!=None:
            vo = seatVo(row[0], row[1], row[2], row[3], row[4])
            return vo

    def select_in_theater(self, theater_code):
        seats = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from seat where theater_code=%s"
        vals = (theater_code,)
        cur.execute(sql, vals)
        for row in cur:
            seats.append(seatVo(row[0], row[1], row[2], row[3], row[4]))
        self.disconnet()
        return seats

    def selectAll(self):
        seats = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from seat"
        cur.execute(sql)
        for row in cur:
            seats.append(seatVo(row[0], row[1], row[2], row[3], row[4]))
        self.disconnet()
        return seats

    def priceupdate(self, theater_code, name, price):
        self.connect()
        cur = self.conn.cursor()
        sql = "update seat set price=%s where theater_code=%s and name=%s"
        vals = (price, theater_code, name)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def availableupdate(self, seat_code, available):
        self.connect()
        cur = self.conn.cursor()
        sql = "update seat set available=%s where code=%s"
        vals = (available, seat_code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def delete(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "delete from seat where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()  # db 닫기

class seatService:
    def __init__(self):
        self.dao = seatDao()
        self.theaterdao = thm.theaterDao()

    def seatCreate(self):
        for i in range(1, 11):
            price = 15000
            if i >= 6:
                price = 10000
            self.dao.insert(seatVo(name='A' + str(i), price=price, available=False, theater_code=self.theaterdao.select_lastCode()))

    def seatavailable(self, theater_code, name):
        self.dao.availableupdate(theater_code, name, "true")
        print('자리선점 처리 완료 [프린트 삭제 예정]')