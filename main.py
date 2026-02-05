import os
from dotenv import load_dotenv
from datetime import date
from crud.users import get_user_by_username, create_user, get_all_users
from crud.table_booking import get_filtered_durations, get_free_tables
from crud.menu import (
    get_daily_menu,
    get_admin_daily_menu,
    admin_get_all_stock,
    add_new_product,
    add_to_daily_menu,
    get_all_products
)
from crud.order import create_order, get_user_orders

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def admin_panel():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. View Food Inventory")
        print("2. User List")
        print("3. Add New Product (To Database)")
        print("4. Add Dish to Daily Menu")
        print("5. View Today's Menu")
        print("0. Exit")

        choice = input("Choice: ")

        if choice == "1":
            stock = admin_get_all_stock()
            if not stock:
                print("\n Menu is empty!")
            else:
                print("\n--- Warehouse Inventory ---")
                for item in stock:
                    print(f"Dish: {item['title']} | Stock: {item['total_amount']} portions")

        elif choice == "2":
            users = get_all_users()
            if not users:
                print("\nNo users found!")
            else:
                print("\n--- USER LIST ---")
                for u in users:
                    print(f"ID: {u['id']} | Username: {u['username']} | Date: {u['created_at']}")

        elif choice == "3":
            title = input("Dish name: ")
            try:
                price = int(input("Price: "))
                desc = input("Description: ")
                if add_new_product(title, price, desc):
                    print("➕ Product added to database!")
            except ValueError:
                print("❗ Error: Price must be a number!")

        elif choice == "4":
            products = get_all_products()
            if not products:
                print("❗ Please add a product first.")
                continue

            print("\n--- PRODUCT LIST ---")
            for p in products:
                print(f"{p['id']}. {p['title']} ({p['price']} USD)")

            try:
                p_id = int(input("Select Product ID: "))
                amount = int(input("Quantity to sell today? "))
                if add_to_daily_menu(p_id, amount):
                    print("➕ Dish added to today's menu!")
            except ValueError:
                print("❗ Error: ID and quantity must be numbers!")

        elif choice == "5":
            menu = get_admin_daily_menu()
            if not menu:
                print("\n❗ Menu for today has not been set yet.")
            else:
                print(f"\n--- TODAY'S MENU ({date.today()}) ---")
                print(f"{'ID':<4} | {'Dish Name':<15} | {'Price':<10} | {'Stock':<8}")
                print("-" * 45)
                for item in menu:
                    print(f"{item['id']:<4} | {item['title']:<15} | {item['price']:<10} | {item['amount']:<8}")

        elif choice == "0":
            break


def user_panel(user):
    while True:
        print(f"\n--- USER PANEL ({user['username']}) ---")
        print("1. Book a Table & Order Food")
        print("2. My Orders")
        print("0. Logout")

        choice = input("Choice: ")
        if choice == "1":
            today = str(date.today())
            slots = get_filtered_durations(today)

            if not slots:
                print("\n❗ No available time slots for today.")
                continue

            print("\n--- AVAILABLE TIME SLOTS ---")
            for s in slots:
                print(f"{s['id']}. {s['from_time']} - {s['to_time']}")

            try:
                dur_id = int(input("\nSelect Time ID: "))

                free_tables = get_free_tables(dur_id, today)
                if not free_tables:
                    print("❗ All tables are booked for this time!")
                    continue

                print(f"Available Tables: {free_tables}")
                table_no = int(input("Select Table Number: "))

                if table_no not in free_tables:
                    print("❗ Error: This table is booked or does not exist!")
                    continue

                menu = get_daily_menu(today)
                if not menu:
                    print("❗ No food available in the menu today.")
                    continue

                print("\n--- TODAY'S MENU ---")
                print(f"{'ID':<4} | {'Dish Name':<15} | {'Price':<10} | {'Stock':<8}")
                print("-" * 45)
                for m in menu:
                    print(f"{m['id']:<4} | {m['title']:<15} | {m['price']:<10} | {m['amount']:<8}")

                m_id = int(input("Select Dish ID: "))
                order_amount = int(input("How many portions? "))

                # The create_order function usually returns success status and a message
                success, msg = create_order(user['id'], m_id, order_amount, dur_id, table_no)
                print(f"\n{msg}")

            except ValueError:
                print("❗ Error: Please enter a valid number!")

        elif choice == "2":
            my_orders = get_user_orders(user['id'])
            if not my_orders:
                print("\n❗ You have no orders yet.")
            else:
                print("\n--- YOUR ORDERS ---")
                for o in my_orders:
                    print(
                        f"ID: {o['id']} | Dish: {o['title']} | Qty: {o['amount']} | Time: {o['from_time']} | Table: {o['table_number']} | Status: {o['status']}")

        elif choice == "0":
            break


def main():
    while True:
        print("\n=== WELCOME TO THE KITCHEN SYSTEM ===")
        print("1. Login")
        print("2. Register")
        print("0. Close Program")

        cmd = input("Choice: ")

        if cmd == "1":
            username = input("Username: ")
            password = input("Password: ")

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                admin_panel()
            else:
                user = get_user_by_username(username)
                if user and user['password'] == password:
                    user_panel(user)
                else:
                    print("❗ Invalid username or password!")

        elif cmd == "2":
            new_user = input("New Username: ")
            new_pass = input("New Password: ")
            if create_user(new_user, new_pass):
                print("✅ Registration successful!")
            else:
                print("This username might already be taken!")

        elif cmd == "0":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()