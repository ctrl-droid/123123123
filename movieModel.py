
import pymysql

class movieVo:
    def __init__(self, code=0, name=None, date=None, director=None, actor=None):
        self.code = code
        self.name = name
        self.date = date
        self.director = director
        self.actor = actor

    def __str__(self):
        return 'code:' + str(self.code)+' / 영화명:' + self.name + ' / 개봉일:' + str(self.date) + ' / 감독:' + self.director+ ' / 배우:' + self.actor

class movieDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='movie_reserve', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into movie(name, date, director, actor) values(%s, %s, %s, %s)"
        vals = (vo.name, vo.date, vo.director, vo.actor)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def selectAll(self):
        movies = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from movie"
        cur.execute(sql)
        for row in cur:
            movies.append(movieVo(row[0], row[1], row[2], row[3], row[4]))
        return movies
        self.disconnect()

    def select(self, name):
        movies=[]
        self.connect()
        cur = self.conn.cursor()
        name = '%'+name+'%'
        sql = "select * from movie where name like %s"
        vals = (name,)
        try:
            cur.execute(sql, vals)
            for row in cur:
                movies.append(movieVo(row[0], row[1], row[2], row[3], row[4]))
            return movies
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update(self, new_date, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "update movie set date=%s where code=%s"
        vals = (new_date, code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "delete from movie where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

class movieService:
    def __init__(self):
        self.dao = movieDao()

    def addMovie(self):
        print('새로운 영화 등록:')
        name = input('영화명:')
        date = input('개봉일:')
        director = input('감독:')
        actor = input('배우:')
        try:
            self.dao.insert(movieVo(name=name, date=date, director=director, actor=actor))
        except Exception as e:
            print(e)
        else:
            print('영화 등록이 완료되었습니다')

    def getAll(self):
        print('----------영화 전체 목록----------')
        movies = self.dao.selectAll()
        if len(movies):
            for m in movies:
                print(m)
        else:
            print('등록된 영화가 없습니다')


    def printList(self, vo_list):
        if vo_list == None or len(vo_list)==0:
            print('검색한 영화가 없습니다')
        else:
            for m in vo_list:
                print(m)

    def getMovie(self):
        print('영화 검색')
        name = input('영화명:')
        vo_list = self.dao.select(name)
        self.printList(vo_list)

    def editMovie(self):    #name을 검색한 결과를 서비스에서 받아서 아까 바꾼 code로 받는 다오를 선택하게끔
        print('영화 정보 수정')
        while True:
            flag = False
            name = input('수정할 영화명을 검색하세요:')
            movies = self.dao.select(name)
            for movie in movies:
                print(movie)
            if len(movies):
                code = int(input('수정할 영화 코드를 입력하세요:'))
                flag = False
                for movie in movies:
                    if movie.code == code:
                        flag = True
                        if flag == True:
                            new_date = input('수정할 개봉일을 입력하세요:')
                    if code != None:
                        self.dao.update(new_date, code)
                        print('수정이 완료되었습니다')
                        return
                    else:
                        print('영화 코드를 잘못 입력 하였습니다')
            else:
                print('검색한 영화가 없습니다')

    def editMovie(self):  # name을 검색한 결과를 서비스에서 받아서 아까 바꾼 code로 받는 다오를 선택하게끔
        print('영화 정보 수정')
        while True:
            name = input('수정할 영화명을 검색하세요:')
            movies = self.dao.select(name)
            for movie in movies:
                print(movie)
            if len(movies):
                code = int(input('수정할 영화 코드를 입력하세요:'))
                for movie in movies:
                    if movie.code == code:
                        new_date = input('수정할 개봉일을 입력하세요:')
                        if code != None:
                            self.dao.update(new_date, code)
                            print('수정이 완료되었습니다')
                            return
                        else:
                            print('영화 코드를 잘못 입력 하였습니다')
            else:
                print('검색한 영화가 없습니다')

    def delMovie(self):
        print('영화 삭제')
        name = input('삭제할 영화명을 검색하세요:')
        movies = self.dao.select(name)
        for movie in movies:
            print(movie)
        code = int(input('삭제할 영화 코드를 입력하세요:'))
        flag = False
        for movie in movies:
            if movie.code == code:
                flag = True
        if flag == True:
            self.dao.delete(code)
            print('삭제가 완료되었습니다')
        else:
            print('영화 코드를 잘못 입력 하였습니다')

