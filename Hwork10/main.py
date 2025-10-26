# --- Base Accounting System (simplified for demonstration) ---
class AccountingSystem:
    def __init__(self):
        self.records = []
        self.balance_amount = 0

    def record(self, message):
        """Record a transaction message."""
        self.records.append(message)
        print(f"[Recorded] {message}")

    def show_records(self):
        """Display all recorded transactions."""
        print("\n--- Transaction Records ---")
        for rec in self.records:
            print(rec)
        print(f"Final Balance: {self.balance_amount}\n")



class Manager(AccountingSystem):
    def __init__(self):
        super().__init__()
        self.tasks = {}  # Maps task names to methods

    def assign(self, name, func):
        """Assign a function (task) by name."""
        self.tasks[name] = func
        print(f"Task '{name}' assigned.")

    def execute(self, name, *args, **kwargs):
        """Execute a task by name."""
        if name in self.tasks:
            print(f"\nExecuting '{name}' operation...")
            return self.tasks[name](*args, **kwargs)
        else:
            print(f"Task '{name}' not found.")


    def log_action(self, action_type):
        """Decorator to log actions automatically."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.record(f"{action_type} of {kwargs.get('amount', 0)} completed.")
                return result
            return wrapper
        return decorator

    def update_balance(self, func):
        """Decorator to automatically update balance."""
        def wrapper(*args, **kwargs):
            amount = kwargs.get('amount', 0)
            if func.__name__ == 'sale':
                self.balance_amount += amount
            elif func.__name__ == 'purchase':
                self.balance_amount -= amount
            return func(*args, **kwargs)
        return wrapper


    @property
    def sale(self):
        @self.update_balance
        @self.log_action("Sale")
        def sale(*args, **kwargs):
            amount = kwargs.get('amount', 0)
            print(f"Selling goods worth {amount}")
        return sale

    @property
    def purchase(self):
        @self.update_balance
        @self.log_action("Purchase")
        def purchase(*args, **kwargs):
            amount = kwargs.get('amount', 0)
            print(f"Purchasing goods worth {amount}")
        return purchase

    @property
    def balance(self):
        def show_balance():
            print(f"Current Balance: {self.balance_amount}")
        return show_balance


# --- Testing the Manager Class ---
if __name__ == "__main__":
    mgr = Manager()

    # Assign actions to manager
    mgr.assign("sale", mgr.sale)
    mgr.assign("purchase", mgr.purchase)
    mgr.assign("balance", mgr.balance)

    # Execute actions
    mgr.execute("sale", amount=500)
    mgr.execute("purchase", amount=200)
    mgr.execute("balance")

    mgr.show_records()
