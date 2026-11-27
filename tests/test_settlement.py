from settlement import calculate_shares, calculate_balances, settle_up

ITEMS = [(24.00, ["Alice", "Bob"]), (15.00, ["Alice"]), (12.00, ["Charlie"])]


def test_shares_with_no_tax_or_tip():
    items = [(10.00, ["Alice", "Bob"])]
    assert calculate_shares(items, 0, 0) == {"Alice": 5.0, "Bob": 5.0}


def test_shares_split_shared_items_and_add_tax_and_tip():
    result = calculate_shares(ITEMS, 0.13, 0.15)
    assert result == {"Alice": 34.56, "Bob": 15.36, "Charlie": 15.36}


def test_balances_when_one_person_paid_everything():
    result = calculate_balances(ITEMS, 0.13, 0.15, {"Alice": 65.28})
    assert result == {"Alice": -30.72, "Bob": 15.36, "Charlie": 15.36}


def test_settle_up_pays_the_person_who_is_owed():
    balances = {"Alice": -30.72, "Bob": 15.36, "Charlie": 15.36}
    assert settle_up(balances) == [
        {"from": "Bob", "to": "Alice", "amount": 15.36},
        {"from": "Charlie", "to": "Alice", "amount": 15.36},
    ]


def test_settle_up_with_everyone_even_returns_nothing():
    assert settle_up({"Alice": 0, "Bob": 0}) == []