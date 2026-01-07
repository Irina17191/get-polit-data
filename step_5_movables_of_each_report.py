import requests
import pandas as pd


headers = {
    "accept": "application/json"
}

df = pd.read_excel("step_2_party_reports_all.xlsx")
report_ids = df["report_id"].tolist()

results = []


for report_id in report_ids:
    url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/movable"
    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка для звіту {report_id}: {response.status_code}")
        continue

    data = response.json()
    data_movable = data.get("results", {}).get("list", [])

    if not data_movable:
        continue


    for item in data_movable:
        results.append({
            "report_id": report_id,
            "id_movable": item.get('id'),
            "report_status": item.get('report_status'),
            "movable_type": item.get('movable_type'),
            "owning_date": item.get('owning_date'),
            "owning_cost": item.get('owning_cost'),
            "description": item.get('description'),
            "manufacturer_name": item.get('manufacturer_name'),
            "trade_mark": item.get('trade_mark'),
            "movable_rights": item.get('movable_rights'),
            "substraction_date": item.get('substraction_date'),
            "created_at": item.get('created_at')
        })

df = pd.DataFrame(results)
df.to_excel("step_5_movables_of_each_party.xlsx", index=False)
print("Дані про звіти збережено у step_5_movables_of_each_party.xlsx")




