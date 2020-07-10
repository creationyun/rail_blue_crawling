import requests
import datetime
import time

start = time.time()

date = "20200305"
station = "%uCD08%uC9C0"
dir = "Seoul_Line_4"
dtdirs = ['04:54:00']

headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Host': 'rail.blue',
    }

for dtdir in dtdirs:
    URL = "https://rail.blue/railroad/logis/getmetrotimetable.aspx?pageIndex={}&date={}&hr=0&min=0&updn=3&station={}&via=&viaopt=0&dir={}&skip=true&do=448&dtdir={}".format(dtdirs.index(dtdir), date, station, dir, dtdir)

    res = requests.post(URL, headers=headers)
    if res.text.split('|')[-7] == '운행 종료':
        break
    dtdirs.append(res.text.split('|')[-10])
    print(res.text)

print("time :", time.time() - start)
