import requests

API_BASE = "http://127.0.0.1:8000"

resp = requests.get(f"{API_BASE}/sportsmen")
if resp.status_code == 200:
    data = resp.json()
    print("Список спортсменов:")
    for s in data["sportsmen"]:
        print(f"{s['ID_Sportsmena']}: {s['Ima']} {s['Familia']} — {s['Razryad']}, клуб {s['Klub']}")
else:
    print("Ошибка получения спортсменов")


resp2 = requests.get(f"{API_BASE}/competitions")
if resp2.status_code == 200:
    data2 = resp2.json()
    print("\nСоревнования:")
    for c in data2["competitions"]:
        print(f"{c['Nazvanie']} ({c['Data_nachala']} — {c['Data_okonchania']}), вид: {c['Vid_sporta']}, объект: {c['Obekt']}")
else:
    print("Ошибка получения соревнований")

comp_name = "Кубок Москвы по футболу"
resp3 = requests.get(f"{API_BASE}/prizers/{comp_name}")
if resp3.status_code == 200:
    data3 = resp3.json()
    print(f"\nПризёры соревнования '{comp_name}':")
    for p in data3["prizers"]:
        print(f"{p['Ima']} {p['Familia']} — место {p['Mesto']}, награда: {p['Nagrada']}")
else:
    print(f"Не удалось получить призёров: {resp3.status_code}")