# звіт партії батьківщина b482ff70-5585-11ef-9197-0fbca96b9f8a
# не віддає дані у розділі paper step_6 (перший ендпоінт де не віддіє дані)
# апі віддає дані у розділі realty step_7
# не віддає дані у розділі transport step_8
# віддає дані у розділі obligations (партія батьківщина) step_9
# також віддає дані у розділі payments
# також віддає дані у розділі payments type


import requests
import pandas as pd
import time


headers = {
    "accept": "application/json"
}



def run_step_8():
    print("Починаю виконувати step_8: transport of each report")


    # Завантажую список ID кожного звіту
    df = pd.read_excel("step_2_party_reports_all.xlsx")
    report_ids = df["report_id"].tolist()

    results = []

    for report_id in report_ids:
        url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/transport"
        response = None

        for attempt in range(10): # максимум 10 спроб
            try:
                response = requests.post(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    break # якщо успішно - виходжу з циклу retry

            except Exception as e:
                print(f"Спроба {attempt+1} не вдалась. Помилка запиту для звіту з report_id: {report_id} - {e}")
                time.sleep(0.3)

        else: # якщо жодна спроба не вдалась
            results.append({
                "report_id": report_id,
                "transport_id": None,
                "party_id": None,
                "office_id": None,
                #"party_report_id": None,
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
                #"party_report_id": None,
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
                # впевнитись щшо party_report_id та report_id ідентичні та видалити наступний рядок
                #"party_report_id": item.get('party_report_id'),
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
    df.to_excel("step_8_transport_of_each_report.xlsx", index=False)
    print("Дані про звіти збережено у step_8_transport_of_each_report.xlsx")



if __name__ == "__main__":
    run_step_8()
