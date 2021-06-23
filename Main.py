from movie_reserve import memModel

def main():
    m = memModel.memDao()
    m.insert(memModel.memVo(id='test1', pwd='1234', name='테스터1', tel='010-1234-5678', point='0'))

main()  