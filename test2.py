try:
    5 // 0
except:
    print("Am error has happened")

print("1")
print("2")
print("3")




import requests
import pandas as pd


headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


def run_step_2():
    print("Починаю виконувати step_2: party reports all")


    # Читаю cvs-файл
    df = pd.read_csv("output/step_1_political_parties_all.csv", encoding="utf-8-sig")

    # Беру колонку 'id'
    party_ids = df["party_id"].tolist()

    results = []

    # Проходимося по кожному id
    for party_id in party_ids:
        url = f'https://politdata.nazk.gov.ua/api/v2/party/{party_id}/reports'
        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            print(f"Помилка для партії {party_id}: {response.status_code}")
            continue

        data = response.json()
        reports_main = data.get('results', {}).get('list', [])


        if not reports_main:
            continue


        for report in reports_main:
            # Основний звіт
            results.append({
                "report_id": report['id'],
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
                        "report_id": report_r['id'],
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

    total_rows = len(df_reports)
    print(f"Всього рядків: {total_rows}")

    unique_reports = df_reports["report_id"].nunique()
    print(f"Унікальних report_id: {unique_reports}")


    if total_rows != unique_reports:
        print(f"Виявлено кількість дублікатів report_id: {total_rows - unique_reports}")

        df_reports = df_reports.drop_duplicates(
            subset=["report_id"],
            keep="first"
        )
        print("Дублікати видалено")
    else:
        print("Дублікатів report_id не виявлено")


    #df_reports.to_excel("step_2_party_reports_all.xlsx", index=False)
    df_reports.to_csv("output/step_2_party_reports_all.csv", index=False, encoding="utf-8-sig")

    print("Дані про звіти збережено у output/step_2_party_reports_all.csv")



if __name__ == "__main__":
    run_step_2()

