import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
import webbrowser
import datetime as dt
from datetime import datetime
from selenium import webdriver

def crawl():
    #초기 변수 세팅
    minus_list=[]
    final_list=[]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 원격 디버깅 포트 설정
    chrome_options.add_argument('--remote-debugging-port=9222')  # 올바른 방법

    chrome_service = webdriver.chrome.service.Service('/usr/local/bin/chromedriver')  # chromedriver 실행 파일 경로로 수정

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # 이제 이 드라이버를 사용하여 크롬을 실행할 수 있습니다.


    # 시간 계산
    today_time = dt.datetime.now()
    stand_time = dt.datetime(1970,1,1)
    minus_day=today_time-stand_time
    day_url=(int(minus_day.days)*86400)-32400-864000
    want_day = 30

    # 로그인
    url="https://ecampus.smu.ac.kr/login.php"
    driver.get(url)


    login_Text = driver.find_element(By.ID, "input-username")
    password_Text=driver.find_element(By.ID, "input-password")
    login_Text.send_keys("jhkim8669")
    password_Text.send_keys("Rlawogus03**")

    login_button=driver.find_element(By.NAME,"loginbutton")
    login_button.click()

    # 로그인
    sub_class1=driver.find_elements(By.CLASS_NAME,"course_box")

    for sub_class in sub_class1:
        sub_class2=sub_class.find_element(By.CLASS_NAME,"course-label")
        sub_class=sub_class.find_element(By.CLASS_NAME,"course-name")
        name=sub_class2.text

        if "SM-Class"==name:
            sub_class=sub_class.find_element(By.TAG_NAME,"h3")
            sub_class=sub_class.text
            sub_class=sub_class.split(" / ")
            sub_class=sub_class[0]
            minus_list.append(sub_class)

    to_replace = [  "(월요일),", "(화요일),", "(수요일),", "(목요일),", "(금요일),", "(토요일),", "(일요일),","년", "월", "일"]
    to_replace_1 = [  "일(월요일)", "일(화요일)", "일(수요일)", "일(목요일)", "일(금요일)", "일(토요일)", "일(일요일)","년", "월"]

    # 일정

    TEXT="진행중인 일정"
    for i in range(1,want_day,1):
        
        driver.get(f"https://ecampus.smu.ac.kr/calendar/view.php?view=day&course=1&time={day_url}")
        div_total=driver.find_element(By.CLASS_NAME,"eventlist")
        day_date=driver.find_element(By.CLASS_NAME,"current")
        day_date=day_date.text
        span_tag = div_total.find_element(By.XPATH, f"//*[contains(text(), '{TEXT}')]")

        ele_list=div_total.find_elements(By.XPATH,"//div[@class='eventlist']/*")

        spanindex=(ele_list.index(span_tag))

        if spanindex!=0:
            div_elements = div_total.find_elements(By.CLASS_NAME,"event")[:spanindex]

            
            for div_ele in div_elements:
                class_name = div_ele.find_element(By.TAG_NAME,"h3")
                class_name= class_name.get_attribute("class")
                
                if class_name=="name":
                    homework_name=div_ele.find_element(By.CLASS_NAME,"name")
                    homework_name=homework_name.text
                    subject="User"
                    # last_time=0
                elif class_name=="referer":
                    homework_name=div_ele.find_element(By.CLASS_NAME,"referer")
                    homework_name=homework_name.find_element(By.TAG_NAME,"a")
                    homework_name=homework_name.text
                    
                    subject= div_ele.find_element(By.CLASS_NAME,"course")
                    subject= subject.find_element(By.TAG_NAME,"a")
                    subject=subject.text
                    
                    
                    # 날짜 데이터 뽑기
                    last_time_all= div_ele.find_element(By.CLASS_NAME,"date")
                    last_time_all=last_time_all.text
                    
                    
                    for replacement in to_replace:
                        last_time_all = last_time_all.replace(replacement, "")
                    for replacement in to_replace_1:
                        day_date = day_date.replace(replacement, "")
                    day_date = day_date.replace(":", "")
                    last_time_all = last_time_all.replace(":", "")
                        
                        
                    if "»" in last_time_all:
                        time_list=last_time_all.split("»")
                        time_list[0]=day_date+time_list[0] 
                    else:
                        time_list=["0000",last_time_all]
                        time_list[0]=str(day_date)+str(time_list[0])
                        
                    if len(time_list[1])<7:
                        time_list[1]=str(day_date)+str(time_list[1])
                        
                    time_list[0]=time_list[0].replace(" ","")
                    time_list[0] = datetime.strptime(time_list[0],"%Y%m%d%H%M")
                    time_list[1]=time_list[1].replace(" ","")
                    time_list[1] = datetime.strptime(time_list[1],"%Y%m%d%H%M")

                if subject not in minus_list:
                    mid_list=[homework_name,subject]

                    for i in range(0,2,1):
                        year = time_list[i].year
                        month = time_list[i].month
                        day = time_list[i].day
                        hour = time_list[i].hour
                        minute = time_list[i].minute
                        time_list_last=[year,month,day,hour,minute]
                        mid_list.append(time_list_last)
                    
                    final_list.append(mid_list)
        day_url=day_url+86400
    print(final_list)
    return(final_list)