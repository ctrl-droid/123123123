import pymysql
import movie_reserve.movieModel as mom
import movie_reserve.seatModel as sem

class theaterVo:
    def __init__(self, code=0, name=None, date=None, movie_code=0):
        self.code = code
        self.name = name
        self.date = date
        self.movie_code = movie_code

    def __str__(self):
        return 'code:' + str(self.code) + ' / 상영관명:' + self.name + ' / 상영날짜:' + self.date + ' / 영화코드:' + str(
            self.movie_code)

class theaterDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='movie_reserve',charset='utf8')

    def disconnet(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into theater(name, date, movie_code) values(%s, %s, %s)"
        vals = (vo.name, vo.date, vo.movie_code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def select(self, name):
        theaters = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from theater where name=%s"
        vals = (name,)
        cur.execute(sql, vals)
        for row in cur:
            theaters.append(theaterVo(row[0], row[1], row[2], row[3]))
        self.disconnet()
        return theaters

    def select_in_movie(self, movie_code):
        theaters = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from theater where movie_code=%s"
        vals = (movie_code,)
        cur.execute(sql, vals)
        for row in cur:
            theaters.append(theaterVo(row[0], row[1], row[2], row[3]))
        self.disconnet()
        return theaters

    def select_lastCode(self):
        self.connect()
        cur = self.conn.cursor()
        sql = "SELECT code FROM theater ORDER BY code DESC LIMIT 1"
        cur.execute(sql)
        row = cur.fetchone()
        self.disconnet()
        if row != None:
            return row[0]

    def selectAll(self):
        theaters = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from theater"
        cur.execute(sql)
        for row in cur:
            theaters.append(theaterVo(row[0], row[1], row[2], row[3]))
        self.disconnet()
        return theaters

    def update(self, code, new_date, new_movie_code):
        self.connect()
        cur = self.conn.cursor()
        sql = "update theater set date=%s, movie_code=%s where code=%s"
        vals = (new_date, new_movie_code, code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def delete(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "delete from theater where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

class theaterService:
    login_id = None

    def __init__(self):
        self.dao = theaterDao()
        self.moviedao = mom.movieDao()
        self.seatservice = sem.seatService()

    def movieselect(self):
        print('----------------영화를 선택해주세요----------------')
        movies = self.moviedao.selectAll()
        for movie in movies:
            print(movie)
        while True:
            movie_code = int(input('선택할 영화 코드를 입력하세요:'))
            for movie in movies:
                if movie.code == movie_code:
                    return movie_code
            print('영화코드를 잘못 입력 하셨습니다.')

    def addTheater(self):
        print('상영관 등록')
        name = input('상영관명:')
        date = input('상영날짜:')
        movie_code = self.movieselect()
        if movie_code != None:
            self.dao.insert(theaterVo(name=name, date=date, movie_code=movie_code))
            self.seatservice.seatCreate()
            print('상영관 등록이 완료되었습니다')
        else:
            print('존해하지 않는 영화코드를 입력하였습니다')

    def theaterAll(self):
        print('상영관 전체 목록')
        theaters = self.dao.selectAll()
        if len(theaters):
            for the in theaters:
                print(the)
        else:
            print('등록된 상영관이 없습니다')

    def printList(self, theater_list):
        if theater_list == None or len(theater_list) == 0:
            print('검색한 상영관이 없습니다')
        else:
            for thr in theater_list:
                print(thr)

    def searchTheather(self):
        print('상영관 검색')
        name = input('상영관명:')
        theater_list = self.dao.select(name)
        self.printList(theater_list)

    def editTheater(self):
        print('상영관 수정')
        print('----------수정할 상영관을 선택해주세요----------')
        theaters = self.dao.selectAll()
        for theater in theaters:
            print(theater)
        code = 0
        while True:
            flag = False
            code = int(input('수정할 상영관 코드 입력:'))
            for theater in theaters:
                if theater.code == code:
                    flag = True
            if flag:
                break
            print('상영관 코드를 잘못 입력 하였습니다.')
        new_date = input('수정할 날짜:')
        new_movie_code = self.movieselect()
        self.dao.update(new_date, new_movie_code, code)

    def delTheater(self):
        print('상영관 삭제')
        print('----------삭제할 상영관을 선택해주세요----------')
        theaters = self.dao.selectAll()
        for theater in theaters:
            print(theater)
        code = 0
        while True:
            flag = False
            code = int(input('삭제할 상영관 코드를 입력하세요:'))
            for theater in theaters:
                if theater.code == code:
                    flag = True
            if flag:
                break
            print('상영관 코드를 잘못 입력 하였습니다')
        self.dao.delete(code)
        print('삭제가 완료되었습니다')