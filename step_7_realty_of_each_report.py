# партія батьківщина b482ff70-5585-11ef-9197-0fbca96b9f8a
# не віддає дані у розділі paper step_6
# апі віддає дані у розділі realty step_7
# не віддає дані у розділі transport step_8
# не віддає дані у розділі obligations
# також віддає дані у розділі payments
# також віддає дані у розділі payments type


import requests
import pandas as pd
import time


headers = {
    "accept": "application/json"
}



def run_step_7():
    print("Починаю виконувати step_7: realty of each report")


    # Завантажую список ID кожного звіту
    df = pd.read_excel("step_2_party_reports_all.xlsx")
    report_ids = df["report_id"].tolist()

    results = []

    for report_id in report_ids:
        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/realty"
        response = None

        for attempt in range(10): #максимум 10 спроб
            try:
                response = requests.post(url, headers=headers)
                if response.status_code == 200:
                    break # якщо успішно - виходжу з циклу retry

            except Exception as e:
                print(f"Спроба {attempt + 1} не вдалась. Помилка запиту для звіту з report_id: {report_id} - {e}")
            #time.sleep(0.3)


        else: # якщо жодна спроба не вдалась
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
                "status": 'OK'
            })

    df = pd.DataFrame(results)
    df.to_excel("step_7_realty_of_each_report.xlsx", index=False)
    print("Дані про звіти збережено у step_7_realty_of_each_report.xlsx")



if __name__ == "__main__":
    run_step_7()
