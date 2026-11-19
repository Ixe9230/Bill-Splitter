from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///billsplitter.db"
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tax_rate = db.Column(db.Float, default=0.13)
    tip_rate = db.Column(db.Float, default=0.15)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database Created!")