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


def run_step_9():
    logging.info("Починаю виконувати step_9: obligations of each report")

    # Завантажую список ID кожного звіту
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/obligations"

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
                "obligation_id": None,
                "report_status": None,
                "object_type_id": None,
                "object_type": None,
                "person_type": None,
                "person_name": None,
                "person_code": None,
                "person_addr": None,
                "owning_cost": None,
                "owning_date": None,
                "owning_reason": None,
                "owning_subject_id": None,
                "end_period_remains_cost": None,
                "created_at": None,
                "status": "FAILED"
            })

            continue


        data = response.json()

        data_obligations = data.get("results", {}).get("list", [])

        if not data_obligations:

            results.append({
                "report_id": report_id,
                "obligation_id": None,
                "report_status": None,
                "object_type_id": None,
                "object_type": None,
                "person_type": None,
                "person_name": None,
                "person_code": None,
                "person_addr": None,
                "owning_cost": None,
                "owning_date": None,
                "owning_reason": None,
                "owning_subject_id": None,
                "end_period_remains_cost": None,
                "created_at": None,
                "status": "NO_ITEMS"
            })

            continue


        for item in data_obligations:

            results.append({
                "report_id": report_id,
                "obligation_id": item.get("id"),
                "report_status": item.get("report_status"),
                "object_type_id": item.get("object_type_id"),
                "object_type": item.get("object_type"),
                "person_type": item.get("person_type"),
                "person_name": item.get("person_name"),
                "person_code": item.get("person_code"),
                "person_addr": item.get("person_addr"),
                "owning_cost": item.get("owning_cost"),
                "owning_date": item.get("owning_date"),
                "owning_reason": item.get("owning_reason"),
                "owning_subject_id": item.get("owning_subject_id"),
                "end_period_remains_cost": item.get("end_period_remains_cost"),
                "created_at": item.get("created_at"),
                "status": "OK"
            })


    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_9_obligations_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_9_obligations_of_each_report.csv")


if __name__ == "__main__":
    run_step_9()
