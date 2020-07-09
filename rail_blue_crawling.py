#!/usr/bin/env python3
''' 초지역 4호선 지연시간 크롤링 '''

# 라이브러리 import
import sys
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# 날짜 입력 (argument가 있을 경우 입력 생략)
argc = len(sys.argv) - 1
if argc < 1:
    print('Date: ', end='')
    crawl_date = input()
else:
    crawl_date = sys.argv[1]

# 파이어폭스를 사용해 오글 로리 사이트 접속.
# 이유: 오글 로리는 Javascript를 사용해 동적으로 전철운행정보를 불러오기 때문.
driver = webdriver.Firefox()
driver.get('https://rail.blue/railroad/logis/metrodriveinfo.aspx?q=7LSI7KeA&c=Seoul_Line_4&date={}&hr=0&min=0&base=1&qv=#!'.format(crawl_date))

# 0.5초마다 스크롤 20번 내리는 효과로 전체 시간표를 불러옴.
for i in range(20):
    print(i)
    driver.execute_script('ScrollLoad();')
    time.sleep(0.5)

# BeautifulSoup 4를 사용해 HTML 코드 크롤링
html = driver.page_source
soup = BeautifulSoup(html, features="lxml")

# train_list: 열차번호 및 지연 정보 등 정차 리스트
# updown_list: 상하행 정보
train_list = soup.find_all("tr", {"id": re.compile(r'trtn_*')})
updown_list = soup.find_all("td", {"class": "tdResult_UpDown"})
# 인덱스를 맞춰주기 위해 타이틀 관련 앞의 2개 제외하고,
# updown에 상행/하행이 아닌 관련 없는 정차(중간중간에 끼어 있음)/통과가 있으면 리스트에서 제외.
updown_list = updown_list[2:]
updown_list = [
    item for item in updown_list if '정차' not in item.text and '통과' not in item.text]

# 본격적인 크롤링 및 상행과 하행을 분류
up_list = {'train': [], 'delay': []}
down_list = {'train': [], 'delay': []}

for i, tr in enumerate(train_list):
    td = tr.find_all("td")
    if '정차' in td[0].text:  # td(0)에 정차가 표시된 경우
        # td에는 열차번호(1)와 지연시간(4)이 있다.
        if '상행' in updown_list[i].text:  # 상행일 경우
            up_list['train'].append(td[1].text.strip())
            up_list['delay'].append(td[4].text.strip())

        if '하행' in updown_list[i].text:  # 하행일 경우
            down_list['train'].append(td[1].text.strip())
            down_list['delay'].append(td[4].text.strip())

# 파일로 저장
# 형식: 날짜_up.csv, 날짜_down.csv
up_df = pd.DataFrame(up_list)
down_df = pd.DataFrame(down_list)
up_df.to_csv(crawl_date + '_up.csv')
down_df.to_csv(crawl_date + '_down.csv')
