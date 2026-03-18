import requests
import pandas as pd
import time
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("steps.log"),
        logging.StreamHandler()
    ]
)


headers = {
    "accept": "application/json"
}


def run_step_7():
    logging.info("Починаю виконувати step_7: realty of each report")

    # Завантажую список ID кожного звіту
    # df = pd.read_excel("step_2_party_reports_all.xlsx")
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/realty"

        success = False

        for attempt in range(10):

            try:

                response = session.post(
                    url,
                    headers=headers,
                    timeout=15,
                    verify=False
                )

                response.raise_for_status()

                success = True
                break

            except requests.exceptions.RequestException as e:

                logging.warning(f"Спроба {attempt + 1} не вдалась для report_id {report_id}: {e}")

                sleep_time = 2 ** attempt
                time.sleep(sleep_time)

                if attempt == 9:
                    failed_ids.append(report_id)
                    logging.error(f"ID {report_id} повністю зафейлився після 10 спроб")

        if not success:

            results.append({
                "report_id": report_id,
                "realty_id": None,
                "report_status": None,
                "object_type": None,
                "object_number": None,
                "owning_date": None,
                "owning_cost": None,
                "owner_code": None,
                "owner_name": None,
                "total_area": None,
                "object_address": None,
                "object_rights": None,
                "substraction_date": None,
                "created_at": None,
                "status": "FAILED"
            })

            continue


        data = response.json()

        data_realty = data.get("results", {}).get("list", [])

        if not data_realty:

            results.append({
                "report_id": report_id,
                "realty_id": None,
                "report_status": None,
                "object_type": None,
                "object_number": None,
                "owning_date": None,
                "owning_cost": None,
                "owner_code": None,
                "owner_name": None,
                "total_area": None,
                "object_address": None,
                "object_rights": None,
                "substraction_date": None,
                "created_at": None,
                "status": "NO_ITEMS"
            })

            continue


        for item in data_realty:

            results.append({
                "report_id": report_id,
                "realty_id": item.get('id'),
                "report_status": item.get('report_status'),
                "object_type": item.get('object_type'),
                "object_number": item.get('object_number'),
                "owning_date": item.get('owning_date'),
                "owning_cost": item.get('owning_cost'),
                "owner_code": item.get('owner_code'),
                "owner_name": item.get('owner_name'),
                "total_area": item.get('total_area'),
                "object_address": item.get('object_address'),
                "object_rights": item.get('object_rights'),
                "substraction_date": item.get('substraction_date'),
                "created_at": item.get('created_at'),
                "status": "OK"
            })


    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_7_realty_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_7_realty_of_each_report.csv")


if __name__ == "__main__":
    run_step_7()
