# партія батьківщина b482ff70-5585-11ef-9197-0fbca96b9f8a
# не віддає дані у розділі paper step_6 (перший ендпоінт де не віддіє дані)
# апі віддає дані у розділі realty step_7
# віддає подекуди дані у розділі transport step_8
# віддає дані у розділі obligations (партія батьківщина) step_9
# також віддає дані у розділі payments
# також віддає дані у розділі payments type


import requests
import pandas as pd
import time


headers = {
    "accept": "application/json"
}



def run_step_9():
    print("Починаю виконувати step_9: obligations of each report")

    # Завантажую список ID кожного звіту
    df = pd.read_excel("step_2_party_reports_all.xlsx")
    report_ids = df["report_id"].tolist()

    results = []

    for report_id in report_ids:
        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/obligations"
        response = None

        for attempt in range(10):  # максимум 10 спроб
            try:
                response = requests.post(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    break  # якщо успішно - виходжу з циклу retry

            except Exception as e:
                print(f"Спроба {attempt + 1} не вдалась. Помилка запиту для звіту з report_id: {report_id} - {e}")
                time.sleep(0.3)

        else:  # якщо жодна спроба не вдалась
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
        data_transport = data.get("results", {}).get("list", [])

        if not data_transport:
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

        for item in data_transport:
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
    df.to_excel("step_9_obligations_of_each_report.xlsx", index=False)
    print("Дані про звіти збережено у step_9_obligations_of_each_report.xlsx")



if  __name__ == "__main__":
    run_step_9()
