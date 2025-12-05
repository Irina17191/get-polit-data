import requests
import pandas as pd


headers = {
    "accept": "application/json"
}


df = pd.read_excel("step_2_party_reports_all.xlsx")

report_ids = df["id"].tolist()

results = []

for report_id in report_ids:
    url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/intangible"
    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка для звіту {report_id}: {response.status_code}")
        continue

    data = response.json()
    data_intangiable = data["results"]["list"]

    if not data_intangiable:
        continue

    for item in data_intangiable:
        results.append({
            "id": report_id,
            "report_status": item.get('report_status'),
            "asset_type": item.get('asset_type'),
            "asset_count": item.get('asset_count'),
            "asset_description": item.get('asset_description'),
            "asset_rights": item.get('asset_rights'),
            "owning_date": item.get('owning_date'),
            "owning_cost": item.get('owning_cost'),
            "substraction_date": item.get('substraction_date'),
            "created_at": item.get('created_at')
        })

df  = pd.DataFrame(results)
df.to_excel("step_3_intangiable_assets_of_each_party.xlsx", index=False)
print("Дані про звіти збережено у step_3_intangiable_assets_of_each_party.xlsx")

