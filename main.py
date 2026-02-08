from datetime import date

from core.config import ADMIN_USERNAME, ADMIN_PASSWORD
# from core.db_settings import execute_query

# from core import models
from crud.users import get_user_by_username, create_user, get_all_users
from crud.table_booking import get_filtered_durations, get_free_tables
from crud.menu import (
    get_daily_menu,
    get_admin_daily_menu,
    admin_get_all_stock,
    add_new_product,
    add_to_daily_menu,
    get_all_products, delete_product, remove_product_from_today_menu
)
from crud.order import create_order, get_user_orders, show_all_orders_by_time, change_order_status, cancel_order


def admin_panel():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. View Food Inventory")
        print("2. User List")
        print("3. Add New Product (To Database)")
        print("4. Delete Product")
        print("5. Add Dish to Daily Menu")
        print("6. View Today's Menu")
        print("7. Remove product from today's menu")
        print("8. Show all orders by time")
        print("9. Change order status")
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
            try:
                product_id = int(input("Enter the product ID to delete: "))
            except ValueError:
                print("❌ Invalid input. Please enter a valid product ID!")
            else:
                if delete_product(product_id):
                    print("✅Product deleted")
                else:
                    print("❌Delete failed or product not found!")



        elif choice == "5":
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

        elif choice == "6":
            menu = get_admin_daily_menu()
            if not menu:
                print("\n❗ Menu for today has not been set yet.")
            else:
                print(f"\n--- TODAY'S MENU ({date.today()}) ---")
                print(f"{'ID':<4} | {'Dish Name':<15} | {'Price':<10} | {'Stock':<8}")
                print("-" * 45)
                for item in menu:
                    print(f"{item['id']:<4} | {item['title']:<15} | {item['price']:<10} | {item['amount']:<8}")

        elif choice == "7":
            try:
                pro_id = int(input("Enter the product ID to remove from today's menu: "))
            except ValueError:
                print("❌ Error: Product ID must be numbers!")

            else:
                if remove_product_from_today_menu(pro_id):
                    print("✅ Product removed successfully!")

                else:
                    print("❌ Failed to remove product from today's menu!")

        elif choice == "8":
            print("\n📋 Orders sorted by scheduled time:\n")
            show_all_orders_by_time()

        elif choice == "9":
            try:
                order_id = int(input("Enter the order ID: "))
            except ValueError:
                print("Order ID must be numbers!")
                continue

            print("Choose order status")
            print("1.pending")
            print("2.done")
            print("3.cancelled")

            status_choice = input("Choice: ")
            status_map = {
                "1": "pending",
                "2": "done",
                "3": "cancelled"
            }
            new_status = status_map.get(status_choice)
            if not new_status:
                print("❌ Invalid status choice!")
                continue
            if change_order_status(order_id, new_status):
                print("✅ Order status updated successfully!")
            else:
                print("❌ Failed to update order status!")

        elif choice == "0":
            break


def user_panel(user):
    while True:
        print(f"\n--- USER PANEL ({user['username']}) ---")
        print("1. View today's menu")
        print("2. Book a Table & Order Food")
        print("3. My Orders")
        print("4. Cancel my order")
        print("0. Logout")

        choice = input("Choice: ")
        if choice == "1":
            menu = get_admin_daily_menu()
            if not menu:
                print("\n❗ Menu for today has not been set yet.")
            else:
                print(f"\n--- TODAY'S MENU ({date.today()}) ---")
                print(f"{'ID':<4} | {'Dish Name':<15} | {'Price':<10} | {'Stock':<8}")
                print("-" * 45)
                for item in menu:
                    print(f"{item['id']:<4} | {item['title']:<15} | {item['price']:<10} | {item['amount']:<8}")

        elif choice == "2":
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

        elif choice == "3":
            my_orders = get_user_orders(user['id'])
            if not my_orders:
                print("\n❗ You have no orders yet.")
            else:
                print("\n--- YOUR ORDERS ---")
                for o in my_orders:
                    print(
                        f"ID: {o['id']} | Dish: {o['title']} | Qty: {o['amount']} | Time: {o['from_time']} | Table: {o['table_number']} | Status: {o['status']}")

        elif choice == "4":
            try:
                ord_id = int(input("\nSelect Order ID: "))

            except ValueError:
                print("❌ Error: Order ID must be numbers!")

            confirm = input("Are you sure you want to cancel this order? (yes/no): ").lower()
            if confirm != "yes":
                print("❎ Cancel aborted")
                continue

            if cancel_order(ord_id):
                print("✅ Order cancelled successfully")
            else:
                print("❌ Order not found or already cancelled")

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
    # execute_query(models.users)
    # execute_query(models.products)
    # execute_query(models.durations)
    # execute_query(models.menu_products)
    # execute_query(models.orders)
    main()

