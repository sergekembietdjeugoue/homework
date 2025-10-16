from csv import excel

from select import select


def display_commands():
    print("\nAvailable commands:")
    print("- balance")
    print("- sale")
    print("- purchase")
    print(" - account")
    print(" - list")
    print(" - warehouse")
    print(" - review")
    print(" - end")


def main():
    account_balance = 0
    warehouse = {}
    operations = []

    display_commands()

    while True:
        command = input("\nEnter command:").strip().lower()

        if command == "balance":
            try:
                amount = float(input("Enter amount to add/subtract:"))
                account_balance += amount
                operations.append(f"Balance: {amount:+}")
            except ValueError:
                print("Invalid amount. Please enter a number.")

        elif command == "sale":
            product = input("Enter product name: ").strip()
            try:
                price = float(input("Enter product price: "))
                quantity = int(input("Enter quantity "))
                if warehouse.get(product, [0, 0])[1] < quantity:
                    print("Not enough stock in warehouse. ")
                else:
                    total = price * quantity
                    account_balance += total
                    warehouse[product][1] -= quantity
                    operations.append(f"Sale: {product}, price {price}, qty {quantity}, total {total}")
            except ValueError:
                print("Invalid input. price must be a number and quantity an integer. ")

        elif command == "purchase":
            product = input("Enter product name: ").strip()
            try:
                price = float(input("Enter product price: "))
                quantity =int(input("Enter quantity: "))
                total = price * quantity
                if account_balance - total < 0:
                    print("Insufficient funds for purchase.")
                else:
                    account_balance -= total
                    if product in warehouse:
                        warehouse[product][0] = price
                        warehouse[product][1] = quantity
                    else:
                        warehouse[product] = [price,quantity]
                    operations.append(f"Purchase: {product}, price {price}, qty {quantity}, total {total}")
            except ValueError:
                print("Invalid input. Price must be a number and quantity an integer. ")

        elif command == "account":
            print(f"Current account balance: {account_balance}")

        elif command == "list":
            if not warehouse:
                print("Warehouse is empty.")
            else:
                print("\nWarehouse inventory:")
                for product, (price, qty) in warehouse.items():
                    print(f"- {product}: price {price}, quantity {qty}")

        elif command == "warehouse":
            product = input("Enter product name: ").strip()
            if product in warehouse:
                price, qty = warehouse[product]
                print(f"{product} -> price: {price}, quantity: {qty}")
            else:
                print(f"{product} not found in warehouse.")
        elif command == "review":
            try:
                from_idx = input("Enter 'from' index (or leave empty): ").strip()
                to_idx = input("Enter 'to' index (or leave empty): ").strip()

                if from_idx == "" and to_idx == "":
                    selected_ops = operations
                else:
                    from_idx = int(from_idx) if from_idx else 0
                    to_idx = int(to_idx) if to_idx else len(operations)
                    if from_idx < 0 or to_idx > len(operations):
                        print("Index out of range")
                        continue
                    selected_ops = operations[from_idx:to_idx]

                print("\nRecorded operations:")
                for i, op in enumerate(selected_ops, 1):
                    print(f"{i}. {op}")

            except ValueError:
                print("Invalid indices. Please enter integers or leave empty.")

        elif command == "end":
            print("Programme terminated")
            break

        else:
            print("Invalid command. Please try again")

        display_commands()






if __name__ == "__main__":
    main()