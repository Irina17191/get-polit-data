import requests
import pandas as pd


headers = {
    "accept": "application/json"
}

df = pd.read_excel("step_2_party_reports_all.xlsx")

report_ids = df["id"].tolist()

results = []

for report_id in report_ids:
    url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/money"
    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка для звіту {report_id}: {response.status_code}")
        continue

    data = response.json()
    data_money = data["results"]["list"]

    if not data_money:
        continue


    for item in data_money:
        results.append({
            "report_id": report_id,   # cb9153e0-e5e3-11ee-96d4-258361b278a8  ід звіту партії
            "id": item.get('id'),
            "report_status": item.get('report_status'),
            "account_type": item.get('account_type'),
            "account_number": item.get('account_number'),
            "account_holder": item.get('account_holder'),
            "account_holder_code": item.get('account_holder_code'),
            "begin_period_balance": item.get('begin_period_balance'),
            "end_period_balance": item.get('end_period_balance'),
            "report_period_income": item.get('report_period_income'),
            "report_period_used_funds": item.get('report_period_used_funds'),
            "created_at": item.get('created_at')
        })

df = pd.DataFrame(results)
df.to_excel("step_4_money_financial_transactions_of_each_party.xlsx", index=False)
print("Дані про звіти збережено у step_4_money_financial_transactions_of_each_party.xlsx")



