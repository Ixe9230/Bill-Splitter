from flask import Flask
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()