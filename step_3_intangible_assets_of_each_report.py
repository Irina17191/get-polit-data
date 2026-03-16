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


def run_step_3():
    logging.info("Починаю виконувати step_3: intangible assets of each report")

    headers = {
        "accept": "application/json"
    }

    #df = pd.read_excel("step_2_party_reports_all.xlsx")
    df = pd.read_csv("output/step_2_party_reports_all.csv", encoding="utf-8-sig")

    report_ids = df["report_id"].tolist()

    results = []

    session = requests.Session()

    failed_ids = []

    for report_id in report_ids:

        success = False

        for attempt in range(5):

            try:

                url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/intangible"

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

        data_intangiable = data.get("results", {}).get("list", [])

        if not data_intangiable:
            continue

        for item in data_intangiable:

            results.append({
                "report_id": report_id,
                "asset_id": item.get('id'),
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


    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_3_intangiable_assets_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про нематеріальні активи для кожного звіту збережено у step_3_intangiable_assets_of_each_report.csv")


if __name__ == "__main__":
    run_step_3()










# import requests
# import pandas as pd
#
#
# def run_step_3():
#     print("Починаю виконувати step_3: intangible assets of each report")
#
#     headers = {
#         "accept": "application/json"
#     }
#
#
#     #df = pd.read_excel("step_2_party_reports_all.xlsx")
#     df = pd.read_csv("step_2_party_reports_all.csv", encoding="utf-8-sig")
#
#     report_ids = df["report_id"].tolist()
#
#     results = []
#
#     for report_id in report_ids:
#         url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/intangible"
#         response = requests.post(url, headers=headers)
#
#         if response.status_code != 200:
#             print(f"Помилка для звіту {report_id}: {response.status_code}")
#             continue
#
#         data = response.json()
#         data_intangiable = data.get("results", {}).get("list", [])
#
#         if not data_intangiable:
#             continue
#
#         for item in data_intangiable:
#             results.append({
#                 "report_id": report_id,
#                 "asset_id": item.get('id'),
#                 "report_status": item.get('report_status'),
#                 "asset_type": item.get('asset_type'),
#                 "asset_count": item.get('asset_count'),
#                 "asset_description": item.get('asset_description'),
#                 "asset_rights": item.get('asset_rights'),
#                 "owning_date": item.get('owning_date'),
#                 "owning_cost": item.get('owning_cost'),
#                 "substraction_date": item.get('substraction_date'),
#                 "created_at": item.get('created_at')
#             })
#
#     df  = pd.DataFrame(results)
#     df.to_csv("output/step_3_intangiable_assets_of_each_report.csv", index=False, encoding="utf-8-sig")
#     print("Дані про нематеріальні активи для кожного звіту збережено у step_3_intangiable_assets_of_each_report.csv")
#
#
#
# if __name__ == "__main__":
#     run_step_3()
