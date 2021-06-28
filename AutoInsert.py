from selenium import webdriver
import movie_reserve.movieModel as mom

class AutoInsert:
    def __init__(self):
        self.driver = None
        self.moviedao = mom.movieDao()

    def getMovieURL(self): # 1차 CGV 박스오피스 예매율 1~6위 까지 영화정보 주소와 이름을 얻어온다.
        self.driver.implicitly_wait(3)
        self.driver.get('http://www.cgv.co.kr/movies/?lt=1&ft=0')
        movie_list = []
        for i in range(1, 3):
            for j in range(1, 4):
                movie = []
                xpath = '// *[ @ id = "contents"] / div[1] / div[3] / ol['+str(i)+'] / li['+str(j)+'] / div[2] / a'
                movie.append(self.driver.find_element_by_xpath(xpath).get_attribute('href'))
                movie.append(self.driver.find_element_by_xpath(xpath).text)
                movie_list.append(movie)
        return movie_list

    def getMovieInfo(self, movie):
        self.driver.implicitly_wait(3)
        self.driver.get(movie[0])
        dateXPath = '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[6]'  # 개봉일
        movie.append(self.driver.find_element_by_xpath(dateXPath).text)
        directorXPath = '// *[ @ id = "select_main"] / div[2] / div[2] / div[3] / dl / dd[1] / a' # 영화감독
        movie.append(self.driver.find_element_by_xpath(directorXPath).text)
        actorXPath = '//*[@id="select_main"]/div[2]/div[2]/div[3]/dl/dd[3]/a[1]' # 배우
        movie.append(self.driver.find_element_by_xpath(actorXPath).text)
        return movie

    def movieCrawler(self):
        print('영화 정보 크롤링 시작....')
        self.driver = webdriver.Chrome(r'./chromedriver')
        movie_list = self.getMovieURL()
        for movie in movie_list:
            movie = self.getMovieInfo(movie)
            self.moviedao.insert(mom.movieVo(name=movie[1], date=movie[2], director=movie[3], actor=movie[4]))
            for row in movie:
                print(row)
        print('영화 정보 DB 등록 완료')