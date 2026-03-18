import requests
import pandas as pd
import time
import json
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


def run_step_6():
    logging.info("Починаю виконувати step_6: paper of each report")

    # Завантажую список ID кожного звіту
    #df = pd.read_excel("step_2_party_reports_all.xlsx")
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/paper"

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
                "info": None,
                "status": "failed"
            })

            continue


        data = response.json()

        data_paper = data.get("results", {}).get("list", [])

        if data_paper:
            info = json.dumps(data_paper, ensure_ascii=False)
        else:
            info = None

        results.append({
            "report_id": report_id,
            "info": info,
            "status": "successful"
        })


    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_6_paper_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_6_paper_of_each_report.csv")


if __name__ == "__main__":
    run_step_6()
