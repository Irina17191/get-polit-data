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


def run_step_4():
    logging.info("Починаю виконувати step_4: money financial transactions of each report")

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

                url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/money"

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

        data_money = data.get("results", {}).get("list", [])

        if not data_money:
            continue

        for item in data_money:

            results.append({
                "report_id": report_id,
                "transaction_id": item.get('id'),
                "report_status": item.get('report_status'),
                "account_type": item.get('account_type'),
                "account_number": item.get('account_number'),
                "account_holder": item.get('account_holder'),
                "account_holder_code": item.get('account_holder_code'),
                "begin_period_balance": item.get('begin_period_balance'),
                "end_period_balance": item.get('end_period_balance'),
                "report_period_income": item.get('report_period_income'),
                "report_period_used_funds": item.get('report_period_used_funds'),
                "created_at": item.get('created_at')
            })

    df = pd.DataFrame(results)

    df.to_csv(
        "output/step_4_money_financial_transactions_of_each_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    session.close()

    logging.info("Дані про звіти збережено у step_4_money_financial_transactions_of_each_report.csv")


if __name__ == "__main__":
    run_step_4()










# import requests
# import pandas as pd
#
#
# headers = {
#     "accept": "application/json"
# }
#
#
#
# def run_step_4():
#     print("Починаю виконувати step_4: money financial transactions of each report")
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
#         url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/money"
#         response = requests.post(url, headers=headers)
#
#         if response.status_code != 200:
#             print(f"Помилка для звіту {report_id}: {response.status_code}")
#             continue
#
#         data = response.json()
#         data_money = data.get("results", {}).get("list", [])
#
#
#         if not data_money:
#             continue
#
#
#         for item in data_money:
#             results.append({
#                 "report_id": report_id,   # cb9153e0-e5e3-11ee-96d4-258361b278a8  ід звіту партії
#                 "transaction_id": item.get('id'),
#                 "report_status": item.get('report_status'),
#                 "account_type": item.get('account_type'),
#                 "account_number": item.get('account_number'),
#                 "account_holder": item.get('account_holder'),
#                 "account_holder_code": item.get('account_holder_code'),
#                 "begin_period_balance": item.get('begin_period_balance'),
#                 "end_period_balance": item.get('end_period_balance'),
#                 "report_period_income": item.get('report_period_income'),
#                 "report_period_used_funds": item.get('report_period_used_funds'),
#                 "created_at": item.get('created_at')
#             })
#
#     df = pd.DataFrame(results)
#     df.to_csv("output/step_4_money_financial_transactions_of_each_report.csv", index=False, encoding="utf-8-sig")
#     print("Дані про звіти збережено у step_4_money_financial_transactions_of_each_report.csv")
#
#
# if __name__ == "__main__":
#     run_step_4()
