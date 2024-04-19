import Database from "better-sqlite3";
import fs from "fs";

const db = new Database('May 11 to April 11.db');

const transactions = db.prepare('SELECT * FROM trades').all();

const traders = {};

for (let i = 0; i < transactions.length; i++) {
    const transaction = transactions[i];
    console.log(`${i + 1}/${transactions.length} buys`);
    const { buyer, card_id, category, price, season, seller, card_name } = transaction;

    if (buyer === seller) {
        continue;
    }

    if (!traders[buyer]) {
        traders[buyer] = {
            "bank": 0,
            "cards": []
        };
    }

    let cardExists = false;
    for (const card of traders[buyer].cards) {
        if (card.card_id === card_id && card.category === category && card.season === season && card.card_name === card_name) {
            card.count += 1;
            cardExists = true;
            break;
        }
    }

    if (!cardExists) {
        traders[buyer].cards.push({
            'card_id': card_id,
            'category': category,
            'season': season,
            'card_name': card_name,
            'count': 1
        });
    }

    traders[buyer].bank -= price;
}

for (let i = 0; i < transactions.length; i++) {
    const transaction = transactions[i];
    console.log(`${i + 1}/${transactions.length} sales`);
    const { buyer, card_id, category, price, season, seller, card_name } = transaction;
    
    if (buyer === seller) {
        continue;
    }

    if (!traders[seller]) {
        traders[seller] = {
            "bank": 0,
            "cards": []
        };
    }

    let cardExists = false;
    for (const card of traders[seller].cards) {
        if (card.card_id === card_id && card.category === category && card.season === season && card.card_name === card_name) {
            if (card.count > 1) {
                card.count -= 1;
            } else {
                traders[seller].cards.splice(traders[seller].cards.indexOf(card), 1);
            }
            cardExists = true;
            break;
        }
    }

    if (price > 10) {
        traders[seller].bank += price - (price - 10) * 0.1;
    } else {
        traders[seller].bank += price;
    }
}

const jsonFile = 'trades.json';
fs.writeFileSync(jsonFile, JSON.stringify(traders, null, 4));
console.log(`Remaining cards saved to ${jsonFile}`);

db.close();