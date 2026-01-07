# Отримання списку цінних паперів, зазначених у звіті політичної партії

import requests
import pandas as pd
import time
import json


headers = {
    "accept": "application/json"
}

# Завантажую список ID кожного звіту
df = pd.read_excel("step_2_party_reports_all.xlsx")
report_ids = df["id"].tolist()

results = []

for report_id in report_ids:
    url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/paper"

    for attempt in range(10): #максимум 10 спроб
        try:
            response = requests.post(url, headers=headers, timeout=15)
            if response.status_code == 200:
                break # якщо успішно - виходжу з циклу retry

        except Exception as e:
            print(f"Спроба {attempt + 1} не вдалась. Помилка запиту для звіту з report_id: {report_id} - {e}")
            #time.sleep(0.3)

    else: # якщо жодна спроба не вдалась
        results.append({
            "report_id": report_id,
            "info": None,
            "status": "failed"
        })
        continue


    data = response.json()
    print("Тип структури:", type(data))
    print("Ключі верхнього рівня:", data.keys())

    # щоб не спамити сервер
    #time.sleep(1)

    data_paper = data.get("results", {}).get("list", [])    # тут буде пустий список?

    if data_paper:
        # функція json.dumps() бере json і перетворює його у рядок (рядок джейсонів)
        info = json.dumps(data_paper, ensure_ascii=False)
    else:
        info = None # якщо data_paper буде пустим списком

    results.append({
        "report_id": report_id,
        "info": info,
        "status": "successful"
    })



df = pd.DataFrame(results)
df.to_excel("step_6_paper_of_each_party.xlsx", index=False)
print("Дані про звіти збережено у step_6_paper_of_each_party.xlsx")


