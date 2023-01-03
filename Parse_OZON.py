import requests
import time
import os

session = requests.Session()

link_login = "https://api-seller.ozon.ru/v1/report/stock/create"
link_report = 'https://api-seller.ozon.ru/v1/report/info'

header = {
    'Client-Id': 'ID',
    'Api-Key': 'API-KEY'
}

req = {
    "language": "DEFAULT"
}

response = session.post(link_login, headers=header, json=req)
time.sleep(15)
data = response.json()
data = data.get('result')
code = data.get('code')
second_req = {
    'code': code
}

second_response = session.post(link_report, headers=header, json=second_req)
time.sleep(15)
link_response = second_response.json()
link_response = link_response.get('result')
link_csv = link_response.get('file')

third_response = session.get(link_csv, headers=header)
time.sleep(15)
result = third_response.text
current_folder = os.getcwd()
with open('C:/Users/79150/Desktop/Telegram_BOT/Ozon_Data.csv', 'w', encoding='utf-8') as f:
    f.write(result)
    f.close()
