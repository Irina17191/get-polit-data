import requests
import pandas as pd


headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


# Читаю Excel-файл (файл має бути в тій самій папці, що й main.py)
df = pd.read_excel("step_1_political_parties_all.xlsx")

# Фільтрую тільки ті партії, де тип == "main"
# Беру колонку 'id'
df_main = df[df["party_type"] == "main"]
party_ids = df_main["id"].tolist()

results = []

# Проходимося по кожному id
for party_id in party_ids:
    url = f'https://politdata.nazk.gov.ua/api/v2/party/{party_id}/reports'
    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка для партії {party_id}: {response.status_code}")
        continue

    data = response.json()
    reports_main = data['results']['list']
    # reports_main = data.get('results', {}).get('list', [])


    if not reports_main:
        continue


    for report in reports_main:
        # Основний звіт
        results.append({
            "id": report['id'],
            "schema_version": report['schema_version'],
            "report_type": report['report_type'],
            "year": report['year'],
            "quarter": report['quarter'],
            "party_id": report['party_id'],
            "main_party_id": report['party_id'],
            "party_code": None,
            "party_name": None,
            "is_party_office": report['is_party_office'],
            "signed_date": report['signed_date'],
            "created_date": report['created_date'],
            "signatory_id": report['signatory_id'],
            "status": None
        })


        if report.get('regional_reports'):
            # Регіональні звіти
            reports_regional = report.get('regional_reports')
            for report_r in reports_regional:
                results.append({
                    "id": report_r['id'],
                    "schema_version": None,
                    "report_type": "regional",
                    "year": report_r['year'],
                    "quarter": report_r['quarter'],
                    "party_id": report_r['party_info']['id'],
                    "main_party_id": report['party_id'],
                    "party_code": report_r['party_info']['code'],
                    "party_name": report_r['party_info']['name'],
                    "is_party_office": None,
                    "signed_date": report_r['signed_date'],
                    "created_date": report_r['created_date'],
                    "signatory_id": None,
                    "status": report_r['status']
                })


# збереження в Excel
df_reports = pd.DataFrame(results)
df_reports.to_excel("step_2_party_reports_all.xlsx", index=False)


print("Дані про звіти збережено у step_2_party_reports_all.xlsx")

