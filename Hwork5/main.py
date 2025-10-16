import os
import ast

# File names
BALANCE_FILE = "balance.txt"
INVENTORY_FILE = "inventory.txt"
HISTORY_FILE = "history.txt"

# Initialize state
balance = 0.0
inventory = {}
history = []

# ----------------- File Handling -----------------
def load_data():
    global balance, inventory, history

    # Balance
    if os.path.exists(BALANCE_FILE):
        try:
            with open(BALANCE_FILE, "r") as f:
                balance = float(f.read().strip())
        except Exception:
            print(" Error reading balance file. Resetting balance to 0.")
            balance = 0.0

    # Inventory
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = ast.literal_eval(f.read().strip())
                if not isinstance(inventory, dict):
                    raise ValueError
        except Exception:
            print(" Error reading inventory file. Resetting inventory.")
            inventory = {}

    # History
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = ast.literal_eval(f.read().strip())
                if not isinstance(history, list):
                    raise ValueError
        except Exception:
            print(" Error reading history file. Resetting history.")
            history = []


def save_data():
    try:
        with open(BALANCE_FILE, "w") as f:
            f.write(str(balance))
        with open(INVENTORY_FILE, "w") as f:
            f.write(str(inventory))
        with open(HISTORY_FILE, "w") as f:
            f.write(str(history))
    except Exception as e:
        print(f" Error saving data: {e}")


# ----------------- Operations -----------------
def add_income(amount):
    global balance
    balance += amount
    history.append(f"Added income: {amount}")
    print(f" Added income {amount}. New balance: {balance}")


def add_expense(amount):
    global balance
    if amount > balance:
        print(" Not enough balance for this expense.")
        return
    balance -= amount
    history.append(f"Expense: {amount}")
    print(f" Expense of {amount} made. New balance: {balance}")


def buy_product(product, price, quantity):
    global balance, inventory
    cost = price * quantity
    if cost > balance:
        print(" Not enough balance to buy product.")
        return
    balance -= cost
    inventory[product] = inventory.get(product, 0) + quantity
    history.append(f"Bought {quantity} x {product} @ {price} each")
    print(f" Bought {quantity} x {product}. Inventory now: {inventory[product]}")


def sell_product(product, price, quantity):
    global balance, inventory
    if product not in inventory or inventory[product] < quantity:
        print(" Not enough inventory to sell.")
        return
    inventory[product] -= quantity
    balance += price * quantity
    history.append(f"Sold {quantity} x {product} @ {price} each")
    print(f" Sold {quantity} x {product}. Inventory left: {inventory[product]}")


def show_history():
    print("\n--- Operation History ---")
    for h in history:
        print(h)


# ----------------- Main -----------------
def main():
    load_data()
    print(" Data loaded. Current balance:", balance)

    while True:
        print("\nOptions: income, expense, buy, sell, history, quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == "income":
            amount = float(input("Enter income amount: "))
            add_income(amount)

        elif choice == "expense":
            amount = float(input("Enter expense amount: "))
            add_expense(amount)

        elif choice == "buy":
            product = input("Product name: ")
            price = float(input("Price per unit: "))
            qty = int(input("Quantity: "))
            buy_product(product, price, qty)

        elif choice == "sell":
            product = input("Product name: ")
            price = float(input("Price per unit: "))
            qty = int(input("Quantity: "))
            sell_product(product, price, qty)

        elif choice == "history":
            show_history()

        elif choice == "quit":
            save_data()
            print(" Data saved. Exiting program.")
            break

        else:
            print(" Invalid option, try again.")


if __name__ == "__main__":
    main()