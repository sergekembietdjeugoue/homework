from functools import wraps

class Manager:
    def __init__(self):
        self.tasks = {}      # mapping of task names to functions
        self.records = []    # keep track of actions

    def assign(self, name, func):
        """Assign a function to a task name."""
        self.tasks[name] = func.__get__(self, Manager)  # bind to this instance

    def run(self, name, *args, **kwargs):
        """Run a task by its assigned name."""
        if name not in self.tasks:
            raise ValueError(f"Task '{name}' not found")
        return self.tasks[name](*args, **kwargs)

    # ------------- DECORATORS -------------
    def operation(self, action):
        """General-purpose decorator for logging operations."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.records.append((action, result))
                print(f"[{action.upper()}] {result}")
                return result
            return wrapper
        return decorator

    def sale(self, func):
        return self.operation("sale")(func)

    def purchase(self, func):
        return self.operation("purchase")(func)

    def balance(self, func):
        return self.operation("balance")(func)


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    manager = Manager()

    @manager.sale
    def sell_item(item, qty):
        return f"Sold {qty} of {item}"

    @manager.purchase
    def buy_item(item, qty):
        return f"Purchased {qty} of {item}"

    @manager.balance
    def show_balance():
        return "Balance checked"

    # Assign tasks dynamically
    manager.assign("sell", sell_item)
    manager.assign("buy", buy_item)
    manager.assign("balance", show_balance)

    # Execute tasks
    manager.run("sell", "laptop", 2)
    manager.run("buy", "mouse", 5)
    manager.run("balance")

    print("\n--- Records ---")
    for action, msg in manager.records:
        print(action, "->", msg)


