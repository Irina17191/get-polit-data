import requests
import pandas as pd


headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


# перевірка звітів для головної партії
main_party_id = '5966f24e-8b67-428d-817f-9b48eb335077'


url = f'https://politdata.nazk.gov.ua/api/v2/party/{main_party_id}/reports'
response = requests.post(url, headers=headers)

data = response.json()
reports_main = data['results']['list']

all_ids = []

for report in reports_main:
    all_ids.append(report["id"])

    if report.get("regional_reports"):
        for regional in report["regional_reports"]:
            all_ids.append(regional["id"])

print("Всі знайдені звіти для головної партії")
for r in all_ids:
    print(r)



# Перевірка звітів для регіональної партії
regional_party_id = '1cf95166-a8c5-4363-a268-36ab0d276b87'

url2 = f'https://politdata.nazk.gov.ua/api/v2/party/{regional_party_id}/reports'
response = requests.post(url2, headers=headers)

data = response.json()
reports_regional = data['results']['list']

all_ids = []

for report in reports_regional:
    all_ids.append(report['id'])

print("Всі знайдені звіти для регіональної партії")
for r in all_ids:
    print(r)

