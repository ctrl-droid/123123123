#영화관리메뉴 -> 영화등록, 영화전체조회, 영화검색, 영화수정, 영화삭제

import pymysql

class movieVo:
    def __init__(self, name=None, date=None, director=None, actor=None):
        self.name = name
        self.date = date
        self.director = director
        self.actor = actor

    def __str__(self):
        return 'name:' + str(self.name) + ' / date:' + str(self.date) + ' / director:' + str(self.director)+ ' / actor:' + str(self.actor)

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
            movies.append(movieVo(row[1], row[2], row[3], row[4]))
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
                movies.append(movieVo(row[1], row[2], row[3], row[4]))
            return movies
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update(self, code, new_date):    #code로 구현
        self.connect()
        cur = self.conn.cursor()
        sql = "update movie set date=%s where code=%d"
        vals = (new_date, code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def delete(self, name):
        name = '%'+name+'%'
        self.dao.select(name)

        movies=[]
        self.connect()
        cur = self.conn.cursor()
        name = '%'+name+'%'
        sql = "select * from movie where name like %s"
        vals = (name,)
        cur.execute(sql, vals)


        sql = "delete from movie where code = %d"
        vals = (name,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()


class movieService:
    def __init__(self):
        self.dao = movieDao()

    def addMovie(self):
        print('영화등록')
        name = input('name:')
        date = input('date:')
        director = input('director:')
        actor = input('actor:')
        try:
            self.dao.insert(movieVo(name=name, date=date, director=director, actor=actor))
        except Exception as e:
            print(e)
        else:
            print('새로운 영화 등록을 완료')

    def getAll(self):
        print('영화전체목록')
        movies = self.dao.selectAll()
        for m in movies:
            print(m)

    def printList(self, vo_list):
        if vo_list == None or len(vo_list)==0:
            print('검색 결과 없음')
        else:
            for m in vo_list:
                print(m)

    def getMovie(self):
        print('영화검색')
        name = input('영화 이름:')
        vo_list = self.dao.select(name)
        self.printList(vo_list)

    def editMovie(self):    #name을 검색한 결과를 서비스에서 받아서 아까 바꾼 code로 받는 다오를 선택하게끔
        print('영화정보수정')
        name = input('수정할 영화 제목:')
        vo = self.dao.select(name)
        if vo==None:
            print('등록되지 않은 영화제목입니다.')
        else:
            code =
            new_date = input('새로운 상영시간:')
            self.dao.update(code, new_date)
            print('영화 정보가 수정되었습니다.')

    def delMovie(self):
        print('영화삭제')
        name = input('삭제할 영화 제목:')
        vo = self.dao.delete(name)
        if vo==None:
            print('등록되지 않은 영화제목입니다.')
        else:
            date = input('새로운 상영시간:')
            self.dao.delete(movieVo(name))
            print('영화가 삭제 되었습니다.')


class Menu:
    def __init__(self):
        self.service = movieService()

    def run(self):
        while True:
            m = input('1.영화등록 2.영화전체조회 3.영화검색 4.영화수정 5.영화삭제 6.메뉴나감')
            if m == '1':
                self.service.addMovie() #print('영화를 입력 받아서 DB에 등록 할수 있도록 구현')
            elif m == '2':
                self.service.getAll()  #('영화목록을 전체 조회가능하도록 구현')
            elif m == '3':
                self.service.getMovie() #print('영화이름(pk X)을 입력 받아서 영화 정보를 출력 하도록 구현')
            elif m == '4':
                self.service.editMovie() #print('영화이름을 입력받아서 영화를 수정하도록 구현 영화코드로 where movie.code')
            elif m == '5':
                self.service.delMovie()  #print('영화이름을 입력받아서 영화를 삭제하도록 구현 영화코드로 where movie.code')
            elif m == '6':
                break

def main():
    pd=Menu()
    pd.run()

main()
