import math 

#Calculates the amount of tax
def calculate_tax(tax_percentage, total_before_tax):
    tax_total = tax_percentage / 100 * total_before_tax
    print(f"The total before tax is ${total_before_tax:.2f}")
    print(f"The tax total is ${tax_total:.2f}")

def check_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter an integer!")

def check_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a number!")

def ask_for_num_items():
    num_of_items = check_valid_int(f"How many items did {name} buy? ")
    people[name]["Number of Items Purchased: "] = num_of_items
    people[name]["Items purchased: "] = []

#Loops depending on the number of items, and asks for each item and price
def item_details(num_of_items):
    subtotal = 0
    for i in range(people[name]["Number of Items Purchased: "]):
        item = input(f"What is the name of item number {i+1}? ")

        cost_of_item = check_valid_float((f"How much did {item} cost? $"))
        people[name]["Items purchased: "].append((f"{item} - ${cost_of_item:.2f}"))
        subtotal += cost_of_item

    people[name]["Subtotal: "] = subtotal
    return subtotal

#Record tax for the person and adds it to total
def record_tax(tax_percentage, subtotal):
    tax = tax_percentage / 100 * subtotal
    people[name]["Tax for items: "] = tax
    people[name]["Tip owed: "] = 0
    people[name]["Total: "] = (tax + subtotal)

#Calculate the amount of tip each person pays
def tip_per_person(people, total_before_tax):
    for name in people:
        percentage_of_total = people[name]["Subtotal: "] / total_before_tax
        tip_person = percentage_of_total * tip
        people[name]["Tip owed: "] += tip_person
        people[name]["Total: "] += tip_person

def print_result():
    print("Summary of purchases and costs:")
    for name in people:
        print(name + ":")
        print("Items purchased:")

        for items in range(people[name]["Number of Items Purchased: "]):
            print(f"{people[name]['Items purchased: '][items]}")

        print(f"You will need to pay ${people[name]['Tax for items: ']:.2f} for tax")
        print(f"You will need to pay ${people[name]['Tip owed: ']:.2f} for tips")

        print(f"Your total payable (including tax and tip) is: ${people[name]['Total: ']:.2f}")
        

if __name__ == "__main__":

    num_of_people = check_valid_int("How many people shared this meal? ")

    people = {}
    total_before_tax = 0

    #Ask about tax%
    tax_percentage = check_valid_float("What is the tax percentage applied? (%) ")

    #Ask about tips
    tip = check_valid_float("How much tip did you give? $")

    #In dictionary people, it will be structured name:{} and inside will be num of items: , Items purchased: [],
    for i in range(num_of_people):
        name = input(f"What is the name of Person #{i+1}? ")
        people[name] = {}
        total = 0
        ask_for_num_items()
        
        total_before_tax = item_details(people[name]["Number of Items Purchased: "])

        record_tax(tax_percentage, people[name]["Subtotal: "])

        #Calculate total amount of tax
        #calculate_tax(tax_percentage, total_before_tax)

    tip_per_person(people, total_before_tax)
    print_result()
