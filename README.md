# Bill Splitter

A REST API that splits a restaurant bill among a group. It handles shared items, tax, tip, and unequal upfront payments, and works out who owes whom.

Status: the backend is complete and tested. A frontend is planned (see Future work).

## Features

- Create bills with custom tax and tip rates
- Add items to a bill and record who shared each one
- Record who paid what upfront, including several payments from the same person
- Calculate each person's balance and a list of payments that settles the bill
- JSON input validation with clear error messages and HTTP status codes

## Tech stack

- Python 3
- Flask and Flask-SQLAlchemy
- SQLite
- pytest

## How it works

1. Each item's price is split evenly among the people who shared it.
2. Tax and tip are applied to each person's own subtotal, so they are shared in proportion to what each person ordered.
3. What each person already paid is subtracted from what they owe. A positive balance means the person still owes money, and a negative balance means they are owed money.
4. A matching step pairs people who owe with people who are owed and produces the payments that settle the bill.

The settlement math lives in `settlement.py` and has no Flask or database code in it, so it can be tested on its own.

## Running it

```bash
git clone https://github.com/Ixe9230/Bill-Splitter.git
cd Bill-Splitter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python app.py                  # creates the database (run once)
flask run --debug --port 5001  # starts the server
```

The API is then available at `http://127.0.0.1:5001`.

## Running the tests

```bash
python -m pytest tests
```

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bills` | Create a bill |
| GET | `/bills` | List all bills |
| GET | `/bills/<id>` | One bill with its items, who shares each, and its payments |
| POST | `/bills/<id>/items` | Add an item to a bill |
| POST | `/bills/<id>/payments` | Record a payment |
| GET | `/bills/<id>/settlement` | Balances and the payments that settle the bill |
| POST | `/people` | Create a person |
| GET | `/people` | List all people |

Errors come back as JSON, like `{"error": "bill not found"}`, with one of these status codes:

| Code | Meaning |
|---|---|
| 201 | Created |
| 400 | Invalid input |
| 404 | Bill not found |
| 409 | That name already exists |

### Request bodies

Create a bill (`tax_rate` and `tip_rate` are optional and default to 0.13 and 0.15, as numbers between 0 and 1):

```json
{"title": "Dinner Out", "tax_rate": 0.13, "tip_rate": 0.15}
```

Add an item (people who do not exist yet are created automatically):

```json
{"name": "Pizza", "price": 24, "people": ["Alice", "Bob"]}
```

Record a payment:

```json
{"person": "Alice", "amount": 40}
```

### Example: a full dinner

A dinner with a $24 pizza shared by Alice and Bob, a $15 burger for Alice, and a $12 salad for Charlie, with 13% tax and 15% tip. The total is $65.28. Alice paid $40 and Bob paid $25.28.

`GET /bills/1/settlement` returns:

```json
{
  "balances": {"Alice": -5.44, "Bob": -9.92, "Charlie": 15.36},
  "bill_id": 1,
  "transfers": [
    {"amount": 5.44, "from": "Charlie", "to": "Alice"},
    {"amount": 9.92, "from": "Charlie", "to": "Bob"}
  ]
}
```

Alice and Bob overpaid, so they are owed money, and Charlie owes the rest.

## Database

Four tables plus a junction table:

- `person`: id, name (unique)
- `bill`: id, title, tax_rate, tip_rate
- `item`: id, name, price, bill_id (foreign key to `bill`)
- `payment`: id, amount_paid, person_id and bill_id (foreign keys)
- `item_shares`: person_id and item_id, a many-to-many link between people and items

A bill has many items and many payments (one-to-many). An item can be shared by many people, and a person can share many items (many-to-many).

## Future work

- A React frontend, with a name picker that suggests existing people and offers to create a new one
- Saved groups of people who eat together often
- One-time guests who are not saved
- Edit and delete endpoints
- Integer cents for money
- Deployment