import movie_reserve.memModel as mem
import movie_reserve.movie as movie

class Menu:
    def __init__(self):
        self.memService = mem.memService()
        self.movieService = movie.movieService

    # 4.내정보 메뉴
    def meminfoMenu(self):
        while True:
            m = input('1.예약정보확인 2.내정보확인 3.내정보수정 4.탈퇴 5.메뉴나감')
            if m == '1':
                pass
            elif m == '2':
                pass
            elif m == '3':
                pass
            elif m == '4':
                pass
            elif m == '5':
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
                self.memService.printmemAll()
            elif m == '2':
                print('회원ID를 입력 받아서 특정 회원을 조회 할 수 있도록 구현')
            elif m == '3':
                print('회원ID를 입력 받아서 특정 회원을 수정 할 수 있도록 구현')
            elif m == '4':
                print('회원ID를 입력 받아서 특정 회원을 삭제 할 수 있도록 구현')
            elif m == '5':
                break

    # 5_2.영화관리 메뉴
    def admin_movieMenu(self):
        while True:
            m = input('1.영화등록 2.영화전체조회 3.영화검색 4.영화수정 5.영화삭제 6.메뉴나감')
            if m == '1':
                self.movieService.addMovie() #print('영화를 입력 받아서 DB에 등록 할수 있도록 구현')
            elif m == '2':
                self.movieService.getAll()  #('영화목록을 전체 조회가능하도록 구현')
            elif m == '3':
                self.movieService.getMovie() #print('영화이름(pk X)을 입력 받아서 영화 정보를 출력 하도록 구현')
            elif m == '4':
                self.movieService.editMovie() #print('영화이름을 입력받아서 영화를 수정하도록 구현 영화코드로 where movie.code')
            elif m == '5':
                self.movieService.delMovie()  #print('영화이름을 입력받아서 영화를 삭제하도록 구현 영화코드로 where movie.code')
            elif m == '6':
                break

    # 5_3.상영관관리 메뉴
    def admin_theaterMenu(self):
        while True:
            m = input('1.상영관등록 2.상영관전체조회 3.상영관검색 4.상영관수정 5.상영관삭제 6.메뉴나감')
            if m == '1':
                print('상영관정보를 입력 받아서 DB에 등록 할수 있도록 구현(영화 CODE를 모르기 때문에 입력 받을시 영화정보를 가져와서 코드를 선택할수 있도록 구현)')
            elif m == '2':
                print('상영관정보목록을 전체 조회가능하도록 구현')
            elif m == '3':
                print('상영관이름(pk X)을 입력 받아서 상영관 정보를 출력 하도록 구현')
            elif m == '4':
                print('상영관이름을 입력받아서 상영관정보를 수정하도록 구현 상영관코드로 where .code')
            elif m == '5':
                print('상영관이름을 입력받아서 상영관정보를 삭제하도록 구현 상영관코드로 where .code')
            elif m == '6':
                break

    def run(self):
        while True:
            m = input('1.영화예약 2.회원가입 3.로그인 4.로그아웃 5.내정보 6.관리자 7.종료')
            if m == '1':
                print('영화 예약(과정) -> table 조인 과정 복잡 ★★★★★')
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