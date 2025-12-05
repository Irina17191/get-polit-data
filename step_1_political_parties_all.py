import requests
import pandas as pd


url = "https://politdata.nazk.gov.ua/api/v2/parties"

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


# функція яка різні чатини адреси складає в один рядок
def to_one_line(parts: list) -> str:
    return ", ".join(filter(None, parts))

def to_one_line_without_comma(parts: list) -> str:
    return " ".join(filter(None, parts))


# список для збереження в Excel
results = []
page = 1
size = 10000

while True:
    payload = {
        "filters": None,
        "order": None,
        "pager": {
            "page": page,
            "size": size
        }
    }

    response = requests.post(url, headers=headers, json=payload)


    if response.status_code != 200:
        print(f"Помилка: {response.status_code}")
        break


    data = response.json()
    polit_parties = data['results']['list']

    if not polit_parties:     # якщо список порожній, зупиняємось
        print("Не має даних у базі")
        break

    for party in polit_parties:

        # head_info
        head_info = ''
        if party.get('head_info'):
            head_info_parts = [
                party['head_info'].get('head_last_name'),
                party['head_info'].get('head_first_name'),
                party['head_info'].get('head_middle_name')
            ]
            head_info = to_one_line_without_comma(head_info_parts)



        # register_address
        register_address = ''
        if party.get('register_address'):
            register_address_parts = [
                party["register_address"].get('country'),
                party['register_address'].get('post_index'),
                party["register_address"].get('region'),
                party["register_address"].get('district'),
                party["register_address"].get('city'),
                party["register_address"].get('street'),
                party["register_address"].get('building'),
                party["register_address"].get('building_part_num'),
                party["register_address"].get('apartments'),
                party["register_address"].get('common'),
                party["register_address"].get('address_uk'),
                party["register_address"].get('address_en')
            ]

            register_address = to_one_line(register_address_parts)



        # actual_address
        actual_address = ''
        if party.get("actual_address"):

            actual_address_parts = [
                party["actual_address"].get("country"),
                party["actual_address"].get("post_index"),
                party["actual_address"].get("region"),
                party["actual_address"].get("district"),
                party["actual_address"].get("city"),
                party["actual_address"].get("street"),
                party["actual_address"].get("building"),
                party["actual_address"].get("building_part_num"),
                party["actual_address"].get("apartments"),
                party["actual_address"].get("common"),
                party["actual_address"].get("address_uk"),
                party["actual_address"].get("address_en")
            ]

            actual_address = to_one_line(actual_address_parts)



        # основні партії
        results.append({
            "id": party['id'],
            "is_active": party['is_active'],
            "party_type": "main",
            "main_party_id": party['id'],
            "code": party['code'],
            "name": party['name'],
            # print(party.get('web_site_url', '')),
            "web_site_url": party.get('web_site_url') or '',
            "actual_address_same_register": party['actual_address_same_register'],
            "created_at": party['created_at'],
            "updated_at": party['updated_at'],
            "email": party['email'],
            "phone": party['phone'],
            "head_info": head_info,
            "register_address": register_address,
            "actual_address": actual_address,
            "parent": party['parent']
        })



        if party.get("regional_offices"):
            regional_offices = party.get("regional_offices")
            for reg_office in regional_offices:
                results.append({
                    "id": reg_office['id'],
                    "is_active": reg_office['is_active'],
                    "party_type": 'regional',
                    "main_party_id": party['id'],
                    "code": reg_office['code'],
                    "name": reg_office['name'],
                    "web_site_url": None,
                    "actual_address_same_register": None,
                    "created_at": None,
                    "updated_at": None,
                    "email": None,
                    "phone": None,
                    "head_info": None,
                    "register_address": None,
                    "actual_address": None,
                    "parent": None
                })




    print(f"Сторінка {page} оброблена, отримано {len(polit_parties)} main партій")
    page += 1


# створюю DataFrame та зберігаємо в Excel
df = pd.DataFrame(results)

###
print(f"Усього зібрано: {len(results)} записів")
print(df['party_type'].value_counts())
##

df.to_excel("step_1_political_parties_all.xlsx", index=False)

print("Дані збережено у step_1_political_parties_all.xlsx")




