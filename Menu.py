import movie_reserve.memModel as mem
import movie_reserve.movieModel as movie
import movie_reserve.theaterModel as theater
import movie_reserve.reserveModel as reserve
import movie_reserve.AutoInsert as ai

class Menu:
    def __init__(self):
        self.memService = mem.memService()
        self.adminmemService = mem.adminmemService()
        self.movieService = movie.movieService()
        self.theaterService = theater.theaterService()
        self.reserveService = reserve.reserveService()
        self.AutoInsert = ai.AutoInsert()

    # 4.내정보 메뉴
    def meminfoMenu(self):
        while True:
            m = input('1.예약정보확인 2.예약취소 3.내정보확인 4.내정보수정 5.탈퇴 6.메뉴나감')
            if m == '1':
                self.reserveService.reserveinfo()
            elif m == '2':
                self.reserveService.reserveCancel()
            elif m == '3':
                self.memService.printMyInfo()
            elif m == '4':
                self.memService.editMyInfo()
            elif m == '5':
                self.memService.delMyInfo()
            elif m == '6':
                break

    # 5.관리자 메뉴
    def adminMenu(self):
        if self.memService.login_id == 'admin':
            while True:
                m = input('1.회원관리 2.영화관리 3.상영관관리 4.메뉴나감')
                if m == '1':
                    self.admin_memMenu()
                elif m == '2':
                    self.admin_movieMenu()
                elif m == '3':
                    self.admin_theaterMenu()
                elif m == '4':
                    break
        else:
            print('admin 계정만 사용 가능합니다.')

    # 5_1.회원관리 메뉴
    def admin_memMenu(self):
        while True:
            m = input('1.전체회원목록 2.회원조회 3.회원정보수정 4.회원삭제 5.메뉴나감')
            if m == '1':
                self.adminmemService.printmemAll()
            elif m == '2':
                self.adminmemService.memsearch()
            elif m == '3':
                self.adminmemService.memupdate()
            elif m == '4':
                self.adminmemService.memdelete()
            elif m == '5':
                break

    # 5_2.영화관리 메뉴
    def admin_movieMenu(self):
        while True:
            m = input('1.영화등록 2.영화전체조회 3.영화검색 4.영화수정 5.영화삭제 6.영화자동등록 7.메뉴나감')
            if m == '1':
                self.movieService.addMovie()
            elif m == '2':
                self.movieService.getAll()
            elif m == '3':
                self.movieService.getMovie()
            elif m == '4':
                self.movieService.editMovie()
            elif m == '5':
                self.movieService.delMovie()
            elif m == '6':
                self.AutoInsert.movieCrawler()
            elif m == '7':
                break

    # 5_3.상영관관리 메뉴
    def admin_theaterMenu(self):
        while True:
            m = input('1.상영관등록 2.상영관전체조회 3.상영관검색 4.상영관수정 5.상영관삭제 6.메뉴나감')
            if m == '1':
                self.theaterService.addTheater()
            elif m == '2':
                self.theaterService.theaterAll()
            elif m == '3':
                self.theaterService.searchTheather()
            elif m == '4':
                self.theaterService.editTheater()
            elif m == '5':
                self.theaterService.delTheater()
            elif m == '6':
                break

    def run(self):
        while True:
            m = input('1.영화예약 2.회원가입 3.로그인 4.로그아웃 5.내정보 6.관리자 7.종료')
            if m == '1':
                self.reserveService.moviereserve()
            elif m == '2':
                self.memService.join()
            elif m == '3':
                self.memService.login()
            elif m == '4':
                self.memService.logout()
            elif m == '5':
                self.meminfoMenu()
            elif m == '6':
                self.adminMenu()
            elif m == '7':
                break