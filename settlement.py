def calculate_shares(items, tax_rate, tip_rate):
    subtotals = {}
    for price, names in items:
        share = price / len(names)
        for name in names:
            subtotals[name] = subtotals.get(name, 0) + share

    return {
        name: round(subtotal * (1 + tax_rate + tip_rate), 2)
        for name, subtotal in subtotals.items()
    }


def calculate_balances(items, tax_rate, tip_rate, payments):
    shares = calculate_shares(items, tax_rate, tip_rate)
    balances = {}
    for name in sorted(set(shares) | set(payments)):
        balances[name] = round(shares.get(name, 0) - payments.get(name, 0), 2)
    return balances

def settle_up(balances):
    debtors = [[name, amount] for name, amount in balances.items() if amount > 0]
    creditors = [[name, -amount] for name, amount in balances.items() if amount < 0]

    transfers = []
    i = 0
    j = 0
    while i < len(debtors) and j < len(creditors):
        amount = round(min(debtors[i][1], creditors[j][1]), 2)
        transfers.append({"from": debtors[i][0], "to": creditors[j][0], "amount": amount})

        debtors[i][1] = round(debtors[i][1] - amount, 2)
        creditors[j][1] = round(creditors[j][1] - amount, 2)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transfers


if __name__ == "__main__":
    items = [(24.00, ["Alice", "Bob"]), (15.00, ["Alice"]), (12.00, ["Charlie"])]
    balances = calculate_balances(items, 0.13, 0.15, {"Alice": 65.28})
    print(calculate_shares(items, 0.13, 0.15))
    print(balances)
    print(settle_up(balances))