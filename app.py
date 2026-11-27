from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///billsplitter.db"
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    items = db.relationship('Item', secondary='item_shares', backref='people')
    payments = db.relationship('Payment', backref='person')

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tax_rate = db.Column(db.Float, default=0.13)
    tip_rate = db.Column(db.Float, default=0.15)
    items = db.relationship('Item', backref='bill')
    payments = db.relationship('Payment', backref='bill')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_paid = db.Column(db.Float, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)

item_shares = db.Table('item_shares',
                       db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
                       db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
                       )

@app.route("/bills", methods=["POST"])
def create_bill():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not isinstance(title, str) or not title.strip(): 
        return jsonify({"error": "title is required"}), 400
    if len(title) > 100:
        return jsonify({"error": "title must be 100 characters or less"}), 400

    bill = Bill(title=title.strip())
    db.session.add(bill)
    db.session.commit()

    return jsonify({
        "id": bill.id,
        "title": bill.title,
        "tax_rate": bill.tax_rate,
        "tip_rate": bill.tip_rate
    }), 201

@app.route("/bills")
def get_bills():
    bills = Bill.query.all()
    return jsonify([
        {"id": b.id, "title": b.title, "tax_rate": b.tax_rate, "tip_rate": b.tip_rate}
        for b in bills
    ])

@app.route("/people", methods=["POST"])
def create_person():
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "name is required"}), 400
    name = name.strip()
    if len(name) > 50:
        return jsonify({"error": "name must be 50 characters or less"}), 400
    if Person.query.filter_by(name=name).first():
        return jsonify({"error": "that name already exists"}), 409

    person = Person(name=name)
    db.session.add(person)
    db.session.commit()

    return jsonify({"id": person.id, "name": person.name}), 201


@app.route("/people")
def get_people():
    people = Person.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in people])

@app.route("/bills/<int:bill_id>/items", methods=["POST"])
def add_item(bill_id):
    bill = db.session.get(Bill, bill_id)
    if bill is None:
        return jsonify({"error": "bill not found"}), 404

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "name is required"}), 400
    name = name.strip()
    if len(name) > 100:
        return jsonify({"error": "name must be 100 characters or less"}), 400

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "price must be a positive number"}), 400

    names = data.get("people")
    if not isinstance(names, list) or not names or not all(isinstance(n, str) for n in names):
        return jsonify({"error": "people must be a non-empty list of names"}), 400

    people = []
    for n in dict.fromkeys(n.strip() for n in names):
        if not n or len(n) > 50:
            return jsonify({"error": "each name must be 1 to 50 characters"}), 400
        person = Person.query.filter_by(name=n).first()
        if person is None:
            person = Person(name=n)
            db.session.add(person)
        people.append(person)
    
    item = Item(name=name, price=price, bill=bill)
    item.people.extend(people)
    db.session.add(item)
    db.session.commit()

    return jsonify({
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "bill_id": bill.id,
        "people": [p.name for p in item.people]
    }), 201

@app.route("/bills/<int:bill_id>/payments", methods=["POST"])
def add_payment(bill_id):
    bill = db.session.get(Bill, bill_id)
    if bill is None:
        return jsonify({"error": "bill not found"}), 404

    data = request.get_json(silent=True) or {}
    person_name = data.get("person")
    amount = data.get("amount")

    if not isinstance(person_name, str) or not person_name.strip():
        return jsonify({"error": "person is required"}), 400
    person_name = person_name.strip()
    if len(person_name) > 50:
        return jsonify({"error": "person must be 50 characters or less"}), 400

    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "amount must be a positive number"}), 400

    person = Person.query.filter_by(name=person_name).first()
    if person is None:
        person = Person(name=person_name)
        db.session.add(person)

    payment = Payment(amount_paid=amount, person=person, bill=bill)
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "id": payment.id,
        "bill_id": bill.id,
        "person": person.name,
        "amount": payment.amount_paid
    }), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()