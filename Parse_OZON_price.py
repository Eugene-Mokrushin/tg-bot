import requests
import time
import openpyxl
import os

current_folder = os.getcwd()
sku_list = []

session = requests.Session()

link_login = "https://api-seller.ozon.ru/v1/report/products/prices/create"
link_report = 'https://api-seller.ozon.ru/v1/report/info'

wb = openpyxl.load_workbook(f'{current_folder}/OZON_DB_ids.xlsx')
ws = wb.active

for cell in ws['A']:
    sku_list.append(cell.value)

sku_list.pop(0)

header = {
    'Client-Id': 'ID',
    'Api-Key': 'API KEY'
}

req = {
    "language": "DEFAULT",
    'sku': sku_list,
    "visibility": "ALL"
}

response = session.post(link_login, headers=header, json=req)
time.sleep(15)
data = response.json()
data = data.get('result')
code = data.get('code')
second_req = {
    'code': code,
}

second_response = session.post(link_report, headers=header, json=second_req)
time.sleep(60)
link_response = second_response.json()
link_response = link_response.get('result')
link_csv = link_response.get('file')

third_response = session.get(link_csv, headers=header)
time.sleep(15)

with open(f'{current_folder}/Ozon_Data_Price.xlsx', 'wb') as f:
    f.write(third_response.content)
    f.close()
