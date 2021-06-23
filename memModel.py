import pymysql

'''
id	varchar(25)
pwd	varchar(45)
name	varchar(45)
tel	varchar(45)
point	int
'''
class memVo:
    def __init__(self, id=None, pwd=None, name=None, tel=None, point=0):
        self.id = id
        self.pwd = pwd
        self.name = name
        self.tel = tel
        self.point = point

    def __str__(self):
        return 'id:' + self.id + ' / pwd:' + self.pwd + ' / name:' + self.name  + ' / tel:' + self.tel + ' / point:' + str(self.point)

class memDao:
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
        sql = "insert into member values(%s, %s, %s, %s, %s)"
        vals = (vo.id, vo.pwd, vo.name, vo.tel, vo.point)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def select(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where id=%s"
        vals = (id,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnet()
        if row!=None:
            vo = memVo(row[0], row[1], row[2], row[3], row[4])
            return vo

    def selectAll(self):
        members = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member"
        cur.execute(sql)
        for row in cur:
            members.append(memVo(row[0], row[1], row[2], row[3], row[4]))
        self.disconnet()
        return members


    def update(self, id, new_pwd, new_tel):
        self.connect()  # db 연결(커넥션을 넣었다 끊었다 해야 지속 선점을 하지 않는다.)
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "update member set pwd=%s, tel=%s where id=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (new_pwd, new_tel, id)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()  # db 닫기

    def delete(self, id):
        self.connect()  # db 연결(커넥션을 넣었다 끊었다 해야 지속 선점을 하지 않는다.)
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = "delete from member where id=%s"  # 변수가 들어갈 위치에 %s와 같은 포맷문자 지정
        vals = (id,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()  # db 닫기

class memService:
    login_id = None

    def __init__(self):
        self.dao = memDao()

    def join(self):
        print('회원가입')
        id = input('id:')
        pwd = input('pwd:')
        name = input('name:')
        tel = input('tel:')
        try:
            self.dao.insert(memVo(id, pwd, name, tel))
        except Exception as e:
            print(e)
        else:
            print('회원가입완료')

    def login(self):
        print('로그인')
        if memService.login_id != None:
            print('이미 로그인 중')
            return
        id = input('id:')
        pwd = input('pwd:')
        vo = self.dao.select(id)
        if vo == None:
            print('없는 아이디')
        else:
            if pwd == vo.pwd:
                print('로그인 성공')
                memService.login_id = id
            else:
                print('패스워드 불일치')

    def logout(self):
        print('로그아웃')
        if memService.login_id == None:
            print('로그인후 사용할수 있습니다.')
            return
        memService.login_id = None;
        print('로그아웃 성공')

    def printmemAll(self):
        print('전체회원목록')
        members = self.dao.selectAll()
        for mem in members:
            print(mem)