# 이미지 크롤링 프로그램

## Install and import dependencies
import urllib.request
import datetime
import time

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus


### scroll_down function definition
def scroll_down(SCROLL_PAUSE_SEC):
    global driver
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            time.sleep(SCROLL_PAUSE_SEC)
            new_height = driver.execute_script("return document.body.scrollHeight")

            try:
                driver.find_element_by_class_name("mye4qd").click()
            except:

               if new_height == last_height:
                   break


        last_height = new_height


# 프로그램 시작, 인트로 기능
print('\n >>> 이미지 파일 크롤링 프로그램입니다. 환영합니다! <<<\n')
now = datetime.datetime.now()
nowDate = now.strftime('      현재 시간 %Y년 %m월 %d일 %H시 %M분 입니다.\n\n')
print(nowDate)
        
# 메인 기능
while True:
    Search_Url = input('검색할 태그를 입력하세요 : ')
    crawl_num = int(input(' >> 크롤링할 이미지 갯수를 입력해 주세요 : '))
    Main_Url = 'https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjgwPKzqtXuAhWW62EKHRjtBvcQ_AUoAXoECBEQAw&biw=768&bih=712'.format(Search_Url)

    driver = webdriver.Chrome("D:\crawl\chromedriver_win32\chromedriver.exe")
    driver.get(Main_Url)

    time.sleep(1)
    SCROLL_PAUSE_SECond = 1
    scroll_down(SCROLL_PAUSE_SECond)
    
    url = Main_Url + quote_plus(Search_Url)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    images = soup.find_all('img', attrs={'class':'rg_i Q4LuWd'})
    print('number of img tags: ', len(images))

    num = 1
    for i in images:
        print('    ※ ',num, '번째 파일 다운로드가 완료되었습니다!')
        try:
            imgUrl = i["src"]
        except:
            imgUrl = i["data-src"]

        with urllib.request.urlopen(imgUrl) as f:
            # 이미지 저장위치 + 파일이름 지정
            with open('./img/' + Search_Url + str(num)+'.jpg','wb') as h:
                img = f.read()
                h.write(img)
        num += 1
        if num > crawl_num:
            break

    print('\n  모든 크롤링이 완료되었습니다! \n ')

    # 종료 확인
    requ = int(input('>>> 프로그램을 종료하려면 1을, 계속 크롤링 하시려면 2를 입력해 주세요 : '))
    print('\n')
    if requ == 2 :
        continue
    else :
        driver.close()
        break