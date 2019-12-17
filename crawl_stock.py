import requests
import json
import csv
from bs4 import BeautifulSoup

URL = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
Ticker = 'VIC'
StrFromDate = '01/12/2009'
StrToDate= '01/12/2018'

StrFromDateTest = '02/12/2018'
StrToDateTest = '01/12/2019'

def crawl(page, fromDate, toDate):
    response = list()
    payload = {
        'pagingInfo.indexPage': page,
        'searchMarketStatisticsView.symbol': Ticker,
        'strFromDate': fromDate,
        'strToDate': toDate
    }
    r = requests.post(URL, data=payload)
    soup = BeautifulSoup(r.content, 'lxml')
    all_history = soup.findAll('ul', {"class": "list_tktt lichsugia"})[0]
    all_history = all_history.findAll('li')

    for transaction in all_history:
        tmp = transaction.findAll('div')
        record = dict()
        record['DATE'] = tmp[0].text.strip()
        # record['thay_doi'] = tmp[1].text.strip()
        record['OPEN'] = tmp[2].text.strip()
        record['HIGH'] = tmp[3].text.strip()
        record['LOW'] = tmp[4].text.strip()
        record['CLOSE'] = tmp[5].text.strip()
        # record['gia_binh_quan'] = tmp[6].text.strip()
        # record['gia_dong_cua_dieu_chinh'] = tmp[7].text.strip()
        
        record['VOLUME'] = tmp[8].text.strip()
        record['kl_thoa_thuan'] = tmp[9].text.strip()
        
        response.append(record)

    response.pop(0)
    return response

# CRAWLING
# 2009 - 2018

result = list()
for page in range(1, 88):
    x = crawl(page, StrFromDate, StrToDate)
    result += x

x = result
f = csv.writer(open(Ticker + "_2009_2018.csv", "w",newline=''))
f.writerow(["DATE", "CLOSE", "TICKER", "OPEN", "HIGH","LOW","VOLUME"])

for x in x:
    f.writerow([x["DATE"],
                x["CLOSE"],
                Ticker,
                x["OPEN"],
                x["HIGH"],
                x["LOW"],
                x["VOLUME"]])

# 2019

result_2019 = list()
for page in range(1, 88):
    y = crawl(page, StrFromDateTest, StrToDateTest)
    result_2019 += y

y = result_2019
f1 = csv.writer(open(Ticker + "_2019.csv", "w",newline=''))
f1.writerow(["DATE", "CLOSE", "TICKER", "OPEN", "HIGH","LOW","VOLUME"])

for y in y:
    f1.writerow([y["DATE"],
                y["CLOSE"],
                Ticker,
                y["OPEN"],
                y["HIGH"],
                y["LOW"],
                y["VOLUME"]])


# open('vndirect.json', 'w').write(json.dumps(result))
# for i in result:
#     print(i)
