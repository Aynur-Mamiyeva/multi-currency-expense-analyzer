import json
import os

class ExpenseAnalyzer:
    def __init__(self, filename="budget_data.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Loads expense data from local JSON storage with error handling."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Warning: Data file corrupted. Initializing fresh dataset.")
        return {"expenses": []}

    def save_data(self):
        """Persists current data to local JSON file."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_expense(self, amount, category, currency, description=""):
        """Adds a new expense entry with structured metadata."""
        expense = {
            "amount": float(amount),
            "category": category.strip().capitalize(),
            "currency": currency.strip().upper(),
            "description": description.strip()
        }
        self.data["expenses"].append(expense)
        self.save_data()
        print(f"✅ Expense added successfully: {amount} {currency} [{category}]")

    def get_mathematical_insights(self):
        """Calculates advanced statistical insights (totals, percentages, highest category, average)."""
        expenses = self.data["expenses"]
        if not expenses:
            return None

        total_spent = sum(exp["amount"] for exp in expenses)
        total_transactions = len(expenses)
        average_expense = total_spent / total_transactions

        category_totals = {}
        for exp in expenses:
            cat = exp["category"]
            category_totals[cat] = category_totals.get(cat, 0.0) + exp["amount"]

        highest_category = max(category_totals, key=category_totals.get) if category_totals else "N/A"

        return {
            "total_spent": total_spent,
            "total_transactions": total_transactions,
            "average_expense": average_expense,
            "category_totals": category_totals,
            "highest_category": highest_category
        }

    def display_report(self):
        """Generates a formatted analytical report for the terminal."""
        insights = self.get_mathematical_insights()
        if not insights:
            print("\n📂 No expenses recorded yet. Start by adding one!\n")
            return

        print("\n" + "=" * 50)
        print(f"{'FINANCIAL ANALYTICAL REPORT':^50}")
        print("=" * 50)
        print(f"Total Transactions : {insights['total_transactions']}")
        print(f"Total Spent        : {insights['total_spent']:.2f}")
        print(f"Average Expense    : {insights['average_expense']:.2f}")
        print(f"Top Expense Driver : {insights['highest_category']} ({insights['category_totals'][insights['highest_category']]:.2f})")
        print("-" * 50)
        print(f"{'Category':<20} | {'Amount':<10} | {'Percentage'}")
        print("-" * 50)

        for cat, total in insights["category_totals"].items():
            percentage = (total / insights["total_spent"]) * 100
            print(f"{cat:<20} | {total:<10.2f} | {percentage:>5.1f}%")
        print("=" * 50 + "\n")


def main():
    tracker = ExpenseAnalyzer()

    while True:
        print("=== MULTI-CURRENCY EXPENSE ANALYZER ===")
        print("1. Add Expense")
        print("2. View Analytical Report")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            try:
                amt = float(input("Enter amount: "))
                cat = input("Enter category (e.g., Food, Transport, Rent): ")
                curr = input("Enter currency (USD, EUR, TRY, RON, etc.): ")
                desc = input("Enter brief description (optional): ")
                tracker.add_expense(amt, cat, curr, desc)
                print("")
            except ValueError:
                print("❌ Error: Please enter a valid numerical amount!\n")

        elif choice == "2":
            tracker.display_report()

        elif choice == "3":
            print("Exiting application. Have a great day!")
            break
        else:
            print("Invalid choice! Please choose between 1 and 3.\n")

if __name__ == "__main__":
    main()
    