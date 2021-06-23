import movie_reserve.memModel as mem

class Menu:
    def __init__(self):
        self.memService = mem.memService()

    # 5. 관리자 메뉴
    def adminMenu(self):
        while True:
            m = input('1.회원관리 2.영화관리 3.상영관관리 4.메뉴나감')
            if m == '1':
                self.userMenu()
            elif m == '2':
                self.admin_movieMenu()
            elif m == '3':
                self.admin_theaterMenu()
            elif m == '4':
                break
    #6-1. 회원관리
    def admin_memMenu(self):
        while True:
            m = input('1.전체회원목록 2.회원조회 3.회원정보수정 4.회원삭제 5.메뉴나감')
            if m == '1':
                pass  #회원목록을 전체리스트로 가져올 수 있도록 구현
            elif m == '2':
                pass  #회원id를 입력받아서 특정 회원을 조회할 수 있도록
            elif m == '3':
                pass  #회원id를 입력받아서 특정 회원을 수정할 수 있도록
            elif m == '4':
                pass  #회원id를 입력받아서 특정 회원을 삭제할 수 있도록
            elif m == '5':
                break

    # 6-2. 영화관리
    def admin_movieMenu(self):
        while True:
            m = input('1.영화등록 2.영화전체조회 3.영화검색 4.영화수정 5.영화삭제 6.메뉴나감')
            if m == '1':
                pass  # 영화를 입력받아서 db에 등록
            elif m == '2':
                pass  # 영화목록을 전체리스트로 가져올 수 있도록 구현
            elif m == '3':
                pass  #영화이름(pk가 아님)을 입력받아서 특정 영화를 검색 할 수 있도록
            elif m == '4':
                pass  #영화이름을 입력받아서 영화를 수정하도록(영화코드로 where movie.code)
            elif m == '5':
                pass  #영화이름을 입력받아서 영화를 삭제하도록(영화코드로 where movie.code)
            elif m == '6':
                break

    #6-3. 상영관관리
    def admin_theaterMenu(self):
        while True:
            m = input('1.상영관등록 2.상영관전체조회 3.상영관검색 4.상영관수정 5.상영관삭제 6.메뉴나감')
            if m == '1':
                pass  # 상영관 정보를 입력 받아서 db에 등록(영화 code를 모르기 때문에 입력 받을 시 영화 정보를 받아와서 코드를 선택할 수 있게)
            elif m == '2':
                pass  # 상영관목록을 전체리스트로 가져올 수 있도록 구현
            elif m == '3':
                pass  #상영관이름(pk가 아님)을 입력받아서 검색 할 수 있도록
            elif m == '4':
                pass  #상영관이름을 입력받아서 영화를 수정하도록(상영관코드로 where theater.code)
            elif m == '5':
                pass  #상영관이름을 입력받아서 영화를 삭제하도록(상영관코드로 where theater.code)
            elif m == '6':
                break


    #사용자 메뉴
    def userMenu(self):
        while True:
            m = input('1.사용자 2.관리자 3.종료')
            if m == '1':
                self.userMenu()
            elif m == '2':
                self.adminMenu()
            elif m == '3':
                break

    def meminfoMenu(self):
        while True:
            m = input('1.예약정보확인 2.내정보확인 3.내정보수정 4.탈퇴 5.메뉴나감')
            if m == '1':
                self.userMenu()
            elif m == '2':
                self.adminMenu()
            elif m == '3':
                self.()
            elif m == '4':
                self.()
            elif m == '5':
                break

    def run(self):
        while True:
            m = input('1.영화예약 2.회원가입 3.로그인 4.로그아웃 5.내정보 6.관리자 7.종료')
            if m == '1':
                pass  #
            elif m == '2':
                pass  #회원정보를 입력 받아서 db에 등록
            elif m == '3':
                pass  #로그인 기능 구현(admin 고려)
            elif m == '4':
                pass  #로그아웃 가능 구현(admin 로그인시 로그아웃 추가)
            elif m == '5':
                self.meminfoMenu()
            elif m == '6':
                self.adminMenu()
            elif m == '7':
                break