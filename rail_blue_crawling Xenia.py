import requests
import datetime
import time

# params 데이터 지정
date = "20200305"               # 날짜
station = "%uCD08%uC9C0"        # 역 이름
dir = "Seoul_Line_4"            # 전철 라인?
dtdirs = ['04:54:00']           # 페이지 받아올 때 가장 처음 데이터의 시간

# headers
headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Host': 'rail.blue',
    }

# 위의 dtdirs 값 반복
for dtdir in dtdirs:
    # URL + 위의 params (dtdirs = URL 파라미터의 pageIndex 값 추가)
    URL = "https://rail.blue/railroad/logis/getmetrotimetable.aspx?pageIndex={}&date={}&hr=0&min=0&updn=3&station={}&via=&viaopt=0&dir={}&skip=true&do=448&dtdir={}".format(dtdirs.index(dtdir), date, station, dir, dtdir)

    # post 요청
    res = requests.post(URL, headers=headers)
    # 운행 종료 발견시 종료
    if res.text.split('|')[-7] == '운행 종료':
        break
    # 받아온 데이터의 마지막 시간을 추가하여 한번 더 load == 스크롤
    dtdirs.append(res.text.split('|')[-10])
    # 출력
    print(res.text)

