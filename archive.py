import sqlite3
import csv
import sys

if len(sys.argv) != 2:
    print("Usage: python archive.py <nation_name>")
    sys.exit(1)

nation_name = sys.argv[1].lower().replace(' ', '_')

con = sqlite3.connect("May 11 to April 11.db")
cursor = con.cursor()

cursor.execute("SELECT * FROM trades WHERE buyer = ? OR seller = ?", (nation_name, nation_name))
transactions = cursor.fetchall()

cards = []

for transaction in transactions:
    buyer, card_id, category, price, season, seller, timestamp, card_name = transaction

    if buyer == nation_name:
        card_exists = False
        for card in cards:
            if card['card_id'] == card_id and card['category'] == category and card['season'] == season and card['card_name'] == card_name:
                card['count'] += 1
                card_exists = True
                break

        if not card_exists:
            cards.append({
                'card_id': card_id,
                'category': category,
                'season': season,
                'card_name': card_name,
                'count': 1
            })

for transaction in transactions:
    buyer, card_id, category, price, season, seller, timestamp, card_name = transaction

    if seller == nation_name:
        for card in cards:
            if card['card_id'] == card_id and card['category'] == category and card['season'] == season and card['card_name'] == card_name:
                if card['count'] > 1:
                    card['count'] -= 1
                    break
                else:
                    cards.remove(card)
                    break

total_card_count = sum(card['count'] for card in cards)
print("Total card count after selling:", total_card_count)
print("Remaining cards after selling:", cards)

category_order = {'l': 0, 'e': 1, 'ur': 2, 'r': 3, 'u': 4, 'c': 5}

sorted_cards = sorted(cards, key=lambda x: (category_order.get(x['category'], float('inf')), -x['count']))
total_card_count = sum(card['count'] for card in sorted_cards)

csv_file = f'{nation_name}.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['card_id', 'category', 'season', 'card_name', 'count'])
    writer.writeheader()
    for card in sorted_cards:
        writer.writerow(card)

print(f"Remaining cards saved to {csv_file}")

cursor.execute("""
    SELECT
        SUM(CASE WHEN buyer = ? THEN -price ELSE price END) AS total_price
    FROM trades
    WHERE buyer = ? OR seller = ?
""", (nation_name, nation_name, nation_name))
total_price_result = cursor.fetchone()
total_price = total_price_result[0] if total_price_result is not None else 0
print("Bank:", total_price)

cursor.execute("""
    SELECT
        SUM(CASE WHEN buyer = ? THEN -price ELSE 0 END) AS amount_spent,
        SUM(CASE WHEN seller = ? THEN price ELSE 0 END) AS amount_gained
    FROM trades
    WHERE buyer = ? OR seller = ?
""", (nation_name, nation_name, nation_name, nation_name))
amount_result = cursor.fetchone()
amount_spent = amount_result[0] if amount_result is not None else 0
amount_gained = amount_result[1] if amount_result is not None else 0
print("Amount Spent:", amount_spent)
print("Amount Gained:", amount_gained)

con.close()
