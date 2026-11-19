from app import app, db, Person, Bill, Item, Payment

with app.app_context():
    db.drop_all()
    db.create_all()

    alice = Person(name="Alice")
    bob = Person(name="Bob")
    charlie = Person(name="Charlie")
    bill = Bill(title="Dinner Out")

    pizza = Item(name="Pizza", price=24.00, bill=bill)
    burger = Item(name="Burger", price=15.00, bill=bill)
    salad = Item(name="Salad", price=12.00, bill=bill)

    pizza.people.extend([alice, bob])
    burger.people.append(alice)
    salad.people.append(charlie)

    p1 = Payment(amount_paid=50.00, person=alice, bill=bill)
    p2 = Payment(amount_paid=30.00, person=bob, bill=bill)

    db.session.add_all([alice, bob, charlie, bill, pizza, burger, salad, p1, p2])
    db.session.commit()

    for item in bill.items:
        print(item.name, "->", [p.name for p in item.people])
    for person in [alice, bob, charlie]:
        print(person.name, "paid", [p.amount_paid for p in person.payments])