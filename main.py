from post import post
from crawl import crawl
from get import get
from datetime import datetime, timezone, timedelta

get_text = get()
crawl_text = crawl()
return_text = []

if (get_text != None):
    for i in range(len(crawl_text)):
        cnt = 0
        for j in range (len(get_text)):
            if get_text[j] in crawl_text[i]:
                print(get_text[j], "는 이미 존재하는 이벤트")
                break
            else:
                cnt+=1
                if (cnt == len(get_text)):
                    return_text.append(crawl_text[i])
else:
    return_text = crawl_text

            


# return_text = [['강의자료1', '컴퓨터프로그래밍Ⅱ(PBL)', [2023, 10, 12, 0, 0], [2023, 10, 15, 23, 59]], 
#                ['강의자료2', '컴퓨터프로그래밍Ⅱ(PBL)', [2023, 10, 12, 0, 0], [2023, 10, 15, 23, 59]], 
#                ['6주차 실습 과제', '알고리즘과게임콘텐츠', [2023, 10, 16, 0, 0], [2023, 10, 16, 23, 59]], 
#                ['중간고사 전 과제 제출', '웹프로그래밍', [2023, 10, 22, 0, 0], [2023, 10, 22, 23, 59]]]

def time_trans(time):
    year = time[0]
    month = time[1]
    day = time[2]
    hour = time[3]
    minute = time[4]

    trans_datetime = (datetime(year, month, day, hour, minute, tzinfo=timezone(timedelta(hours=9)))).isoformat()
    print(trans_datetime)
    return trans_datetime

for i in range(len(return_text)):
    temp = return_text[i]
    summary = temp[0]
    description = temp[1]
    end_time = time_trans(temp[3])
    
    # Calculate start_time as one hour before end_time
    end_time_datetime = datetime.fromisoformat(end_time)
    start_time_datetime = end_time_datetime - timedelta(hours=1)
    start_time = start_time_datetime.isoformat()

    # Store start_time and end_time in a list
    post(summary, description, start_time, end_time)