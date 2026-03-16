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


def run_step_5():
    logging.info("Починаю виконувати step_5: movables of each report")

    # df = pd.read_excel("step_2_party_reports_all.xlsx")
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        success = False

        for attempt in range(5):

            try:

                url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/movable"

                response = session.post(
                    url,
                    headers=headers,
                    timeout=10,
                    verify=False
                )

                response.raise_for_status()

                success = True
                break

            except requests.exceptions.RequestException as e:

                logging.warning(f"Спроба {attempt+1} для {report_id} неуспішна {e}")

                sleep_time = 2 ** attempt
                time.sleep(sleep_time)

                if attempt == 4:
                    failed_ids.append(report_id)
                    logging.error(f"ID {report_id} повністю зафейлився після 5 спроб")

        if not success:
            continue

        data = response.json()

        data_movable = data.get("results", {}).get("list", [])

        if not data_movable:
            continue

        for item in data_movable:

            results.append({
                "report_id": report_id,
                "movable_id": item.get('id'),
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

    df.to_csv(
        "output/step_5_movables_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_5_movables_of_each_report.csv")


if __name__ == "__main__":
    run_step_5()




# import requests
# import pandas as pd
#
#
# headers = {
#     "accept": "application/json"
# }
#
#
# def run_step_5():
#     print("Починаю виконувати step_5: movables of each report")
#
#
#     # df = pd.read_excel("step_2_party_reports_all.xlsx")
#     df = pd.read_csv("step_2_party_reports_all___.csv", encoding="utf-8-sig")
#     report_ids = df["report_id"].tolist()
#
#     results = []
#
#
#     for report_id in report_ids:
#         url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/movable"
#         response = requests.post(url, headers=headers)
#
#         if response.status_code != 200:
#             print(f"Помилка для звіту {report_id}: {response.status_code}")
#             continue
#
#         data = response.json()
#         data_movable = data.get("results", {}).get("list", [])
#
#         if not data_movable:
#             continue
#
#
#         for item in data_movable:
#             results.append({
#                 "report_id": report_id,
#                 "movable_id": item.get('id'),
#                 "report_status": item.get('report_status'),
#                 "movable_type": item.get('movable_type'),
#                 "owning_date": item.get('owning_date'),
#                 "owning_cost": item.get('owning_cost'),
#                 "description": item.get('description'),
#                 "manufacturer_name": item.get('manufacturer_name'),
#                 "trade_mark": item.get('trade_mark'),
#                 "movable_rights": item.get('movable_rights'),
#                 "substraction_date": item.get('substraction_date'),
#                 "created_at": item.get('created_at')
#             })
#
#     df = pd.DataFrame(results)
#     df.to_csv("output/step_5_movables_of_each_report.csv", index=False, encoding="utf-8-sig")
#     print("Дані про звіти збережено у step_5_movables_of_each_report.csv")
#
#
#
# if __name__ == "__main__":
#     run_step_5()
