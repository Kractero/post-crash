import sqlite3
import json
import time

start_time = time.time()

con = sqlite3.connect("May 11 to April 11.db")
cursor = con.cursor()

traders = {}

cursor.execute("SELECT * FROM trades")
transactions = cursor.fetchall()

for transaction in transactions:
    buyer, card_id, category, price, season, seller, timestamp, card_name = transaction

    if buyer == seller:
        continue

    if buyer not in traders:
        traders[buyer] = {"bank": 0, "cards": {}}

    traders[buyer]["bank"] -= price

    if card_id not in traders[buyer]["cards"]:
        traders[buyer]["cards"][card_id] = {
            "card_name": card_name,
            "seasons": {}
        }

    if season not in traders[buyer]["cards"][card_id]["seasons"]:
        traders[buyer]["cards"][card_id]["seasons"][season] = {
            "category": category,
            "count": 1
        }
    else:
        traders[buyer]["cards"][card_id]["seasons"][season]["count"] += 1

    if seller not in traders:
        traders[seller] = {"bank": 0, "cards": {}}

    if card_id not in traders[seller]["cards"]:
        traders[seller]["cards"][card_id] = {
            "card_name": card_name,
            "seasons": {}
        }

    if season not in traders[seller]["cards"][card_id]["seasons"]:
        traders[seller]["cards"][card_id]["seasons"][season] = {
            "category": category,
            "count": -1
        }
    else:
        traders[seller]["cards"][card_id]["seasons"][season]["count"] -= 1

    if price > 10:
        traders[seller]["bank"] += price - (price - 10) * 0.1
    else:
        traders[seller]["bank"] += price

for trader in traders.values():
    for card in trader["cards"].values():
        card["seasons"] = {season: data for season, data in card["seasons"].items() if data["count"] > 0}
        total_count = sum(season["count"] for season in card["seasons"].values())
        card["count"] = total_count

    trader["cards"] = [card for card in trader["cards"].values() if card["count"] > 0]

    category_order = {'l': 0, 'e': 1, 'ur': 2, 'r': 3, 'u': 4, 'c': 5}
    # trader["cards"] = sorted(trader["cards"], key=lambda x: (category_order.get(x['category']), -x["count"]))


for trader in traders.values():
    trader["bank"] = max(trader["bank"], 0)

json_file = 'trades.json'
with open(json_file, 'w') as json_output:
    json.dump(traders, json_output, indent=4)

print(f"Remaining traders saved to {json_file}")

con.close()

end_time = time.time()
execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
