import requests
import json
import csv
from bs4 import BeautifulSoup

URL = 'https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/lich-su-gia.shtml'
Ticker = 'VCB'
StrFromDate = '01/12/2009'
StrToDate= '02/12/2019'

def crawl(page):
    response = list()
    payload = {
        'pagingInfo.indexPage': page,
        'searchMarketStatisticsView.symbol': Ticker,
        'strFromDate': StrFromDate,
        'strToDate': StrToDate
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


result = list()
for page in range(1, 88):
    x = crawl(page)
    result += x

x = result
f = csv.writer(open("test.csv", "w",newline=''))
f.writerow(["DATE", "CLOSE", "TICKER", "OPEN", "HIGH","LOW","VOLUME"])

for x in x:
    f.writerow([x["DATE"],
                x["CLOSE"],
                Ticker,
                x["OPEN"],
                x["HIGH"],
                x["LOW"],
                x["VOLUME"]])

# open('vndirect.json', 'w').write(json.dumps(result))
# for i in result:
#     print(i)
