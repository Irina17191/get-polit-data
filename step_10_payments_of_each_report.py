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

# Завантажую список ID кожного звіту
df = pd.read_excel("step_2_party_reports_all.xlsx")
report_ids = df["id"].tolist()

results = []

for report_id in report_ids:
    url = f"https://politdata.nazk.gov.ua/api/v2/party/report/{report_id}/payments"
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
            "payment_id": None,
            ###### перевірити чи співпадає з першим полем та видалити
            "report_id": None,
            "group_code": None,
            "payment_type": None,
            "payment_code": None,
            "payment_number": None,
            "payment_amount": None,
            "payment_currency": None,
            "payment_reason": None,
            "payment_purpose": None,
            "payment_operation_date": None,
            "payment_instruction_date": None,
            "payment_description": None,
            "refund_date": None,
            "refund_amount": None,
            "refund_budget_amount": None,
            "refund_reason": None,
            "refund_purpose": None,
            "refund_description": None,
            "payer_type": None,
            "payer_name": None,
            "payer_code": None,
            "payer_birthday": None,
            "payer_address": None,
            "payer_account_type": None,
            "payer_account_iban": None,
            "payer_bank_code": None,
            "payer_bank_name": None,
            "payer_bank_address": None,
            "receiver_type": None,
            "receiver_name": None,
            "receiver_code": None,
            "receiver_birthday": None,
            "receiver_address": None,
            "receiver_account_type": None,
            "receiver_account_iban": None,
            "receiver_bank_code": None,
            "receiver_bank_name": None,
            "receiver_bank_address": None,
            "created_at": None,
            "updated_at": None,
            "status": "FAILED"
        })
        continue

    data = response.json()
    data_payments = data.get("results", {}).get("list", [])

    if not data_payments:
        results.append({
            "report_id": report_id,
            "payment_id": None,
            ###### перевірити чи співпадає з першим полем та видалити
            "report_id": None,
            "group_code": None,
            "payment_type": None,
            "payment_code": None,
            "payment_number": None,
            "payment_amount": None,
            "payment_currency": None,
            "payment_reason": None,
            "payment_purpose": None,
            "payment_operation_date": None,
            "payment_instruction_date": None,
            "payment_description": None,
            "refund_date": None,
            "refund_amount": None,
            "refund_budget_amount": None,
            "refund_reason": None,
            "refund_purpose": None,
            "refund_description": None,
            "payer_type": None,
            "payer_name": None,
            "payer_code": None,
            "payer_birthday": None,
            "payer_address": None,
            "payer_account_type": None,
            "payer_account_iban": None,
            "payer_bank_code": None,
            "payer_bank_name": None,
            "payer_bank_address": None,
            "receiver_type": None,
            "receiver_name": None,
            "receiver_code": None,
            "receiver_birthday": None,
            "receiver_address": None,
            "receiver_account_type": None,
            "receiver_account_iban": None,
            "receiver_bank_code": None,
            "receiver_bank_name": None,
            "receiver_bank_address": None,
            "created_at": None,
            "updated_at": None,
            "status": "NO_ITEMS"
        })
        continue

    for item in data_payments:
        results.append({
            "report_id": report_id,
            "payment_id": item.get("payment_id"),
            ###### перевірити чи співпадає з першим полем та видалити
            "report_id": item.get("report_id"),
            "group_code": item.get("group_code"),
            "payment_type": item.get("payment_type"),
            "payment_code": item.get("payment_code"),
            "payment_number": item.get("payment_number"),
            "payment_amount": item.get("payment_amount"),
            "payment_currency": item.get("payment_currency"),
            "payment_reason": item.get("payment_reason"),
            "payment_purpose": item.get("payment_purpose"),
            "payment_operation_date": item.get("payment_operation_date"),
            "payment_instruction_date": item.get("payment_instruction_date"),
            "payment_description": item.get("payment_description"),
            "refund_date": item.get("refund_date"),
            "refund_amount": item.get("refund_amount"),
            "refund_budget_amount": item.get("refund_budget_amount"),
            "refund_reason": item.get("refund_reason"),
            "refund_purpose": item.get("refund_purpose"),
            "refund_description": item.get("refund_description"),
            "payer_type": item.get("payer_type"),
            "payer_name": item.get("payer_name"),
            "payer_code": item.get("payer_code"),
            "payer_birthday": item.get("payer_birthday"),
            "payer_address": item.get("payer_address"),
            "payer_account_type": item.get("payer_account_type"),
            "payer_account_iban": item.get("payer_account_iban"),
            "payer_bank_code": item.get("payer_bank_code"),
            "payer_bank_name": item.get("payer_bank_name"),
            "payer_bank_address": item.get("payer_bank_address"),
            "receiver_type": item.get("receiver_type"),
            "receiver_name": item.get("receiver_name"),
            "receiver_code": item.get("receiver_code"),
            "receiver_birthday": item.get("receiver_birthday"),
            "receiver_address": item.get("receiver_address"),
            "receiver_account_type": item.get("receiver_account_type"),
            "receiver_account_iban": item.get("receiver_account_iban"),
            "receiver_bank_code": item.get("receiver_bank_code"),
            "receiver_bank_name": item.get("receiver_bank_name"),
            "receiver_bank_address": item.get("receiver_bank_address"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "status": "OK"
        })

df = pd.DataFrame(results)
df.to_excel("step_10_payments_of_each_report.xlsx", index=False)
print("Дані про звіти збережено у step_10_payments_of_each_report.xlsx")



