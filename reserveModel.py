import pymysql
import movie_reserve.memModel as mem
import movie_reserve.movieModel as mom
import movie_reserve.seatModel as sem
import movie_reserve.theaterModel as thm

class reserveVo:
    def __init__(self, code=None, payment=None, movie_code=None, theater_code=None, seat_code=None, member_id=None):
        self.code = code
        self.payment = payment
        self.movie_code = movie_code
        self.theater_code = theater_code
        self.seat_code = seat_code
        self.member_id = member_id

    def __str__(self):
        return '예약코드:' + str(self.code) + ' / 결제정보:' + self.payment + ' / 영화코드' + str(self.movie_code)\
               + ' / 상영관코드:' + str(self.theater_code) + ' / 좌석코드:' + str(self.seat_code) + ' / 회원아이디:' + self.member_id

class reserveInfoVo:
    def __init__(self, code=None, payment=None, movie_name=None, theater_name=None, seat_name=None, member_id=None):
        self.code = code
        self.payment = payment
        self.movie_name = movie_name
        self.theater_name = theater_name
        self.seat_name = seat_name
        self.member_id = member_id

    def __str__(self):
        return '예약코드:' + str(self.code) + ' / 영화이름:' + str(self.movie_name)+ ' / 상영관이름:' + str(self.theater_name) \
               + ' / 좌석이름:' + str(self.seat_name) + ' / 결제정보:' + self.payment

class reserveDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='movie_reserve', charset='utf8')

    # db 닫는 함수
    def disconnet(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = "insert into reserve(payment, movie_code, theater_code, seat_code, member_id) values(%s, %s, %s, %s, %s)"
        vals = (vo.payment, vo.movie_code, vo.theater_code, vo.seat_code, vo.member_id)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()

    def select(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from reserve where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnet()
        if row!=None:
            vo = reserveVo(row[0], row[1], row[2], row[3], row[4], row[5])
            return vo

    def selectMember(self, member_id):
        reserveinfos = []
        self.connect()
        cur = self.conn.cursor()
        sql = """
            SELECT r.code, r.payment, m.name, t.name, s.name, r.member_id
            FROM reserve r 
            JOIN movie m
            ON r.movie_code = m.code
            JOIN theater t
            ON r.theater_code = t.code
            JOIN seat s
            ON r.seat_code = s.code
            where r.member_id = %s"""
        vals = (member_id,)
        cur.execute(sql, vals)
        for row in cur:
            reserveinfos.append(reserveInfoVo(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.disconnet()
        return reserveinfos

    def selectAll(self):
        reserves = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from reserve"
        cur.execute(sql)
        for row in cur:
            reserves.append(reserveVo(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.disconnet()
        return reserves

    def update(self, code, payment, movie_code, theater_code, seat_code, member_id):
        self.connect()
        cur = self.conn.cursor()
        sql = "update reserve set payment=%s, movie_code=%s, theater_code=%s, seat_code=%s where code=%s"
        vals = (payment, movie_code, theater_code, seat_code, member_id, code)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()  # db 닫기

    def delete(self, code):
        self.connect()
        cur = self.conn.cursor()
        sql = "delete from reserve where code=%s"
        vals = (code,)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnet()  # db 닫기

class reserveService:
    def __init__(self):
        self.memdao = mem.memDao()
        self.moviedao = mom.movieDao()
        self.theaterdao = thm.theaterDao()
        self.seatdao = sem.seatDao()
        self.reservedao = reserveDao()

    def movieselect(self):
        print('--------------- 영화를 선택해주세요 ---------------')
        movies = self.moviedao.selectAll()
        for movie in movies:
            print(movie)
        while True:
            movie_code = int(input('영화코드:'))
            for movie in movies:
                if movie.code == movie_code:
                    return movie_code
            print('영화코드를 잘못 입력 하셨습니다.')

    def theaterselect(self, movie_code):
        print('-------------- 상영관을 선택해주세요 --------------')
        theaters = self.theaterdao.select_in_movie(movie_code)
        for theater in theaters:
            print(theater)
        while True:
            theater_code = int(input('상영관코드:'))
            for theater in theaters:
                if theater.code == theater_code:
                    return theater_code
            print('상영관코드를 잘못 입력 하셨습니다.')

    def seatselect(self, theater_code):
        audiences = 0
        while True:
            print('------- 예약할 인원을 입력해주세요(최대 4명) --------')
            num = int(input('인원:'))
            if num >0 and num <= 4:
                audiences = num
                break
            else:
                print('예약할 인원을 잘못 입력하였습니다. 다시 입력해주세요')

        seats = self.seatdao.select_in_theater(theater_code) # 좌석 조회
        for seat in seats: # 좌석 출력
            print(seat)
        seat_list = []
        for i in range(1, audiences + 1):
            select_code = self.audienceselect(seats, seat_list)
            seat_list.append(select_code)
        return seat_list

    def audienceselect(self, seats, seat_list):
        while True:
            print(str(len(seat_list)+1) + '번째 좌석을', end='')
            name = input('선택:')
            select_code = None
            for seat in seats: # 좌석이름 선택 또는 예약된 좌석 선택시
                if seat.name == name and seat.available == False:
                    select_code = seat.code
                    break
            if select_code != None:  # 선택된 좌석 코드가 있다면
                errflag = False
                for seatcode in seat_list: # 이미 선택한 좌석중에 현재 선택한 좌석이 있는지 비교(있으면 True)
                    if select_code == seatcode:
                        errflag = True
                if errflag:
                    print('이미 선택한 좌석입니다.')
                else:
                    return select_code
            else:
                print('좌석을 잘못 선택 또는 이미 예약된 좌석입니다.')

    def payment(self, seat_list):
        pay = None
        while True:
            print('------------ 결제 방식을 선택해 주세요 ------------')
            check = input('1.카드 2.계좌이체:')
            if check == '1':
                pay = '카드'
                break
            elif check == '2':
                pay = '계좌이체'
                break
            else:
                print('다시 선택해 주세요')

        totalprice = 0  # 선택된 좌석의 총 금액
        for code in seat_list:
            seatvo = self.seatdao.select(code)
            totalprice += seatvo.price
        print('------------------- 결제 진행 -------------------')
        print('결제 하실 금액은' + str(totalprice) + '원 입니다. 결제 하시겠습니까?')
        while True:
            check = input('1.결제 2.예약취소: ')
            if check == '1':
                return pay + ' ' + str(totalprice) + '원'
            elif check == '2':
                return None
            else:
                print('다시 선택해 주세요')

    def moviereserve(self):
        loginid = mem.memService.login_id
        if loginid == None:
            print('로그인후 사용할수 있습니다.')
            return
        print('영화 예약')
        movie_code = self.movieselect()
        theater_code = self.theaterselect(movie_code)
        seat_list = self.seatselect(theater_code)
        payment = self.payment(seat_list)
        if payment != None:
            for seat_code in seat_list:
                self.reservedao.insert(reserveVo(payment=payment, movie_code=movie_code, theater_code=theater_code, seat_code=seat_code, member_id=loginid))
                self.seatdao.availableupdate(seat_code=seat_code, available=True)
            print('예약이 완료 되었습니다.')
        else:
            print('예약이 취소 되었습니다.')

    def reserveinfo(self):
        loginid = mem.memService.login_id
        if loginid == None:
            print('로그인후 사용할수 있습니다.')
            return
        print(loginid, '님의 예약 목록 입니다.')
        reserve = self.reservedao.selectMember(loginid)
        for row in reserve:
            print(row)

    def reserveselect(self, loginid):
        print('------------------- 예약 목록 -------------------')
        reserve = self.reservedao.selectMember(loginid)
        for row in reserve:
            print(row)
        while True:
            reserve_code = int(input('취소할 예약코드를 입력 해주세요:'))
            for row in reserve:
                if row.code == reserve_code:
                    return reserve_code
            print('예약코드를 잘못 입력 하셨습니다.')

    def reserveCancel(self):
        loginid = mem.memService.login_id
        if loginid == None:
            print('로그인후 사용할수 있습니다.')
            return
        reserve_code = self.reserveselect(loginid)
        reserveVo = self.reservedao.select(reserve_code)
        self.seatdao.availableupdate(seat_code=reserveVo.seat_code, available=False)
        self.reservedao.delete(reserve_code)
        print('예약 취소가 완료되었습니다.')
