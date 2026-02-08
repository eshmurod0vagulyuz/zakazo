from core.db_settings import execute_query


def decrease_menu_stock(menu_product_id: int, order_amount: int) -> bool:
    """
    Decreases the food quantity in the menu_products table.
    """
    query = """
        UPDATE menu_products 
        SET amount = amount - %s 
        WHERE id = %s AND amount >= %s;
    """

    result = execute_query(query, (order_amount, menu_product_id, order_amount))
    return result is True


def get_menu_inventory_for_admin():
    """
    For Admin: Returns food titles, remaining stock, and menu dates.
    """
    query = """
        SELECT p.title, m.amount, m.dete_of_menu 
        FROM menu_products m
        JOIN products p ON m.product_id = p.id
        ORDER BY m.dete_of_menu DESC;
    """

    return execute_query(query, fetch="all")


def get_daily_menu(menu_date: str):
    """Shows today's menu and remaining stock for users."""
    query = """
        SELECT m.id as menu_id, p.title, p.price, m.amount 
        FROM menu_products m
        JOIN products p ON m.product_id = p.id
        WHERE m.dete_of_menu::date = %s AND m.amount > 0;
    """
    return execute_query(query, (menu_date,), fetch="all")


def get_admin_daily_menu():
    """Shows today's menu in detail for the admin."""
    query = """
        SELECT m.id, p.title, p.price, m.amount 
        FROM menu_products m
        JOIN products p ON m.product_id = p.id
        WHERE m.dete_of_menu = CURRENT_DATE
        ORDER BY m.id;
    """
    return execute_query(query, fetch="all")


def update_menu_amount(menu_product_id: int, quantity: int):
    """Reduces food quantity after a sale."""
    query = """
        UPDATE menu_products 
        SET amount = amount - %s 
        WHERE id = %s AND amount >= %s;
    """
    return execute_query(query, (quantity, menu_product_id, quantity))


def admin_get_all_stock():
    query = """
        SELECT p.title, SUM(m.amount) as total_amount
        FROM menu_products m
        JOIN products p ON m.product_id = p.id
        WHERE m.dete_of_menu = CURRENT_DATE
        GROUP BY p.title;
    """
    result = execute_query(query, fetch="all")
    return result if result else []


def add_new_product(title: str, price: int, description: str = ""):
    """
    Updates price if product title exists,
    otherwise creates a new product.
    """
    check_query = "SELECT id FROM products WHERE LOWER(title) = LOWER(%s);"
    existing_product = execute_query(check_query, (title,), fetch="one")

    if existing_product:

        update_query = """
            UPDATE products 
            SET price = %s, description = %s 
            WHERE id = %s;
        """
        execute_query(update_query, (price, description, existing_product['id']))
        print(f"[!] '{title}' already exists, price has been updated.")
        return existing_product['id']
    else:
        insert_query = """
            INSERT INTO products (title, price, description) 
            VALUES (%s, %s, %s) RETURNING id;
        """
        new_id = execute_query(insert_query, (title, price, description), fetch="one")
        print(f"[+] New product '{title}' Added")
        return new_id

def add_to_daily_menu(product_id: int, amount: int):
    check_query = """
        SELECT id FROM menu_products 
        WHERE product_id = %s AND dete_of_menu = CURRENT_DATE;
    """
    existing_item = execute_query(check_query, (product_id,), fetch="one")

    if existing_item:
        update_query = """
            UPDATE menu_products 
            SET amount = amount + %s 
            WHERE id = %s;
        """
        return execute_query(update_query, (amount, existing_item['id']))
    else:
        insert_query = """
            INSERT INTO menu_products (product_id, amount, dete_of_menu) 
            VALUES (%s, %s, CURRENT_DATE);
        """
        return execute_query(insert_query, (product_id, amount))

def get_all_products():
    """Gets the list of all products"""
    query = "SELECT id, title, price FROM products;"
    return execute_query(query, fetch="all")

def delete_product(product_id: int) -> bool:
    """
    Deletes product from database
    :param product_id: product id
    :return:
    """
    query = " DELETE FROM products WHERE id = %s"
    params: tuple = (product_id,)
    return execute_query(query=query, params=params, fetch="one")

def remove_product_from_today_menu(product_id: int):
    """
    Removes product from today's menu
    :param product_id:
    :return:
    """
    query =  """
    DELETE FROM menu_products
    WHERE id = %s
    AND date_of_menu = CURRENT_DATE
    """
    params: tuple = (product_id,)
    result = execute_query(query=query, params=params, fetch="one")
    return result

