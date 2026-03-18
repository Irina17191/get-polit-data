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


def run_step_8():
    logging.info("Починаю виконувати step_8: transport of each report")

    # Завантажую список ID кожного звіту
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/transport"

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

                logging.warning(f"Спроба {attempt+1} не вдалась для report_id {report_id}: {e}")

                sleep_time = 2 ** attempt
                time.sleep(sleep_time)

                if attempt == 9:
                    failed_ids.append(report_id)
                    logging.error(f"ID {report_id} повністю зафейлився після 10 спроб")

        if not success:

            results.append({
                "report_id": report_id,
                "transport_id": None,
                "party_id": None,
                "office_id": None,
                "report_status": None,
                "transport_type_id": None,
                "transport_type": None,
                "owning_subject_id": None,
                "owning_date": None,
                "owning_cost": None,
                "object_number": None,
                "transport_brand": None,
                "transport_model": None,
                "production_year": None,
                "object_rights_id": None,
                "object_rights": None,
                "substraction_date": None,
                "created_at": None,
                "status": "FAILED"
            })

            continue


        data = response.json()

        data_transport = data.get("results", {}).get("list", [])

        if not data_transport:

            results.append({
                "report_id": report_id,
                "transport_id": None,
                "party_id": None,
                "office_id": None,
                "report_status": None,
                "transport_type_id": None,
                "transport_type": None,
                "owning_subject_id": None,
                "owning_date": None,
                "owning_cost": None,
                "object_number": None,
                "transport_brand": None,
                "transport_model": None,
                "production_year": None,
                "object_rights_id": None,
                "object_rights": None,
                "substraction_date": None,
                "created_at": None,
                "status": "NO_ITEMS"
            })

            continue


        for item in data_transport:

            results.append({
                "report_id": report_id,
                "transport_id": item.get('id'),
                "party_id": item.get('party_id'),
                "office_id": item.get('office_id'),
                "report_status": item.get('report_status'),
                "transport_type_id": item.get('transport_type_id'),
                "transport_type": item.get('transport_type'),
                "owning_subject_id": item.get('owning_subject_id'),
                "owning_date": item.get('owning_date'),
                "owning_cost": item.get('owning_cost'),
                "object_number": item.get('object_number'),
                "transport_brand": item.get('transport_brand'),
                "transport_model": item.get('transport_model'),
                "production_year": item.get('production_year'),
                "object_rights_id": item.get('object_rights_id'),
                "object_rights": item.get('object_rights'),
                "substraction_date": item.get('substraction_date'),
                "created_at": item.get('created_at'),
                "status": "OK"
            })


    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_8_transport_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_8_transport_of_each_report.csv")


if __name__ == "__main__":
    run_step_8()
