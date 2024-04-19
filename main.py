import sqlite3
import json
import time
start_time = time.time()
con = sqlite3.connect("May 11 to April 11.db")
cursor = con.cursor()

traders = {}

cursor.execute("SELECT * FROM trades")
transactions = cursor.fetchall()

for i, transaction in enumerate(transactions):
    print(f"{str(i)}/{len(transactions)} buys")
    buyer, card_id, category, price, season, seller, timestamp, card_name = transaction

    # Skip same buyer and seller
    if buyer == seller:
        continue

    if buyer not in traders:
        traders[buyer] = {
            "bank": 0,
            "cards": []
        }

    card_exists = False
    for card in traders[buyer]['cards']:
        if card['card_id'] == card_id and card['category'] == category and card['season'] == season and card['card_name'] == card_name:
            card['count'] += 1
            card_exists = True
            break

    if not card_exists:
        traders[buyer]['cards'].append({
            'card_id': card_id,
            'category': category,
            'season': season,
            'card_name': card_name,
            'count': 1
        })

    traders[buyer]["bank"] -= price

for i, transaction in enumerate(transactions):
    print(f"{str(i)}/{len(transactions)} sales")
    buyer, card_id, category, price, season, seller, timestamp, card_name = transaction
    
    if buyer == seller:
        continue

    if seller not in traders:
        traders[seller] = {
            "bank": 0,
            "cards": []
        }

    card_exists = False
    for card in traders[seller]['cards']:
        if card['card_id'] == card_id and card['category'] == category and card['season'] == season and card['card_name'] == card_name:
            if card['count'] > 1:
                card['count'] -= 1
            else:
                traders[seller]['cards'].remove(card)
            card_exists = True
            break

    if price > 10:
        traders[seller]["bank"] += price - (price - 10) * 0.1
    else:
        traders[seller]["bank"] += price

# for trader in traders:
#     print ("sorting by rarity for " + trader + " and computing bank values")
#     # total_card_count = sum(card['count'] for card in traders[trader]['cards'])

#     # category_order = {'l': 0, 'e': 1, 'ur': 2, 'r': 3, 'u': 4, 'c': 5}

#     # sorted_cards = sorted(traders[trader]['cards'], key=lambda x: (category_order.get(x['category'], float('inf')), -x['count']))
#     # total_card_count = sum(card['count'] for card in sorted_cards)

#     cursor.execute("""
#         SELECT
#             SUM(CASE WHEN buyer = ? THEN -price ELSE                 CASE 
#                     WHEN price > 10 THEN price - (price - 10) * 0.1
#                     ELSE price
#                 END END) AS total_price
#         FROM trades
#         WHERE buyer = ? OR seller = ?
#     """, (trader, trader, trader))
#     total_price_result = cursor.fetchone()
#     total_price = total_price_result[0] if total_price_result is not None else 0
#     traders[trader]["bank"] = 0 if total_price is None or total_price < 0 else total_price,

json_file = 'trades.json'
with open(json_file, 'w') as json_output:
    json.dump(traders, json_output, indent=4)

print(f"Remaining cards saved to {json_file}")

con.close()
end_time = time.time()

execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
