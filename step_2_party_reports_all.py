import requests    # 1cf95166-a8c5-4363-a268-36ab0d276b87
import pandas as pd
import time
import logging
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# стандартний логінг
#logging.basicConfig(
#    filename="steps.log",
#    level=logging.INFO,
#    format="%(asctime)s - %(levelname)s - %(message)s"
#)


# щоб логування і записувалось у файл і виводилось у консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("steps.log"),
        logging.StreamHandler()
    ]
)




headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


def run_step_2():
    logging.info("Починаю виконувати step_2: party reports all")


    # Читаю cvs-файл
    df = pd.read_csv("output/step_1_political_parties_all.csv", encoding="utf-8-sig")

    # Беру колонку 'id'
    party_ids = df["party_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []


    # Проходимося по кожному id
    for party_id in party_ids:
        success = False
        for attempt in range(5):
            try:
                url = f'https://politdata.nazk.gov.ua/api/v2/party/{party_id}/reports'
                response = session.post(url, headers=headers, timeout=10, verify=False) # verify=False - відключення перевірки SSL сертифікатів
                response.raise_for_status()
                success = True
                break
            except requests.exceptions.RequestException as e:
                logging.warning(f"Спроба {attempt+1} для {party_id} неуспішна {e}")

                sleep_time = 2 ** attempt
                time.sleep(sleep_time)

                if attempt == 4:
                    failed_ids.append(party_id)
                    logging.error(f"ID {party_id} повністю зафейлився після 5 спроб")


        if not success:
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
    logging.info(f"Всього рядків: {total_rows}")

    unique_reports = df_reports["report_id"].nunique()
    logging.info(f"Унікальних report_id: {unique_reports}")


    if total_rows != unique_reports:
        logging.info(f"Виявлено кількість дублікатів report_id: {total_rows - unique_reports}")

        df_reports = df_reports.drop_duplicates(
            subset=["report_id"],
            keep="first"
        )
        logging.info("Дублікати видалено")
    else:
        logging.info("Дублікатів report_id не виявлено")


    #df_reports.to_excel("step_2_party_reports_all.xlsx", index=False)
    df_reports.to_csv("output/step_2_party_reports_all.csv", index=False, encoding="utf-8-sig")

    session.close()

    logging.info("Дані про звіти збережено у output/step_2_party_reports_all.csv")



if __name__ == "__main__":
    run_step_2()
