# Отримання списку цінних паперів, зазначених у звіті політичної партії

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





# # Отримання списку цінних паперів, зазначених у звіті політичної партії
#
# import requests
# import pandas as pd
# import time
# import json
#
#
# headers = {
#     "accept": "application/json"
# }
#
#
#
# def run_step_6():
#     print("Починаю виконувати step_6: paper of each report")
#
#
#     # Завантажую список ID кожного звіту
#     #df = pd.read_excel("step_2_party_reports_all.xlsx")
#     df = pd.read_csv("step_2_party_reports_all___.csv", encoding="utf-8-sig")
#     report_ids = df["report_id"].tolist()
#
#     results = []
#
#     for report_id in report_ids:
#         url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/paper"
#
#         for attempt in range(10): #максимум 10 спроб
#             try:
#                 response = requests.post(url, headers=headers, timeout=15)
#                 if response.status_code == 200:
#                     break # якщо успішно - вихід з циклу retry
#
#             except Exception as e:
#                 print(f"Спроба {attempt + 1} не вдалась. Помилка запиту для звіту з report_id: {report_id} - {e}")
#                 #time.sleep(0.3)
#
#         else: # якщо жодна спроба не вдалась
#             results.append({
#                 "report_id": report_id,
#                 "info": None,
#                 "status": "failed"
#             })
#             continue
#
#
#         data = response.json()
#         print("Тип структури:", type(data))
#         print("Ключі верхнього рівня:", data.keys())
#
#         # щоб не спамити сервер
#         #time.sleep(1)
#
#         data_paper = data.get("results", {}).get("list", [])    # тут буде пустий список
#
#         if data_paper:
#             # функція json.dumps() бере json і перетворює його у рядок (рядок джейсонів)
#             info = json.dumps(data_paper, ensure_ascii=False)
#         else:
#             info = None # якщо data_paper буде пустим списком
#
#         results.append({
#             "report_id": report_id,
#             "info": info,
#             "status": "successful"
#         })
#
#
#
#     df = pd.DataFrame(results)
#     df.to_csv("output/step_6_paper_of_each_report.csv", index=False, encoding="utf-8-sig")
#     print("Дані про звіти збережено у step_6_paper_of_each_report.csv")
#
#
#
# if __name__ == "__main__":
#     run_step_6()
