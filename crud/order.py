from core.db_settings import execute_query
from crud.menu import update_menu_amount


def create_order(user_id, menu_product_id, amount, duration_id, table_number):
    """Create a new order and reduce the number of meals"""

    stock_updated = update_menu_amount(menu_product_id, amount)

    if not stock_updated:
        return False, "Not enough food!"


    query = """
        INSERT INTO orders (user_id, menu_product_id, amount, duration_id, table_number, status, order_type)
        VALUES (%s, %s, %s, %s, %s, 'pending', 'dine_in')
    """
    params = (user_id, menu_product_id, amount, duration_id, table_number)

    success = execute_query(query, params)
    if success:
        return True, "Order accepted!"
    return False, "Error"


def get_user_orders(user_id):
    """View all user orders"""
    query = """
        SELECT o.id, p.title, o.amount, d.from_time, o.table_number, o.status
        FROM orders o
        JOIN menu_products m ON o.menu_product_id = m.id
        JOIN products p ON m.product_id = p.id
        JOIN durations d ON o.duration_id = d.id
        WHERE o.user_id = %s;
    """
    result = execute_query(query, (user_id,), fetch="all")
    return result if result else []

def show_all_orders_by_time():
    """Show all orders by time"""
    query = """
    SELECT o.id, u.username, p.title, o.amount, o.table_number, o.status, o.order_type, o.created_at
    FROM orders o
    JOIN users u ON o.user_id = u.id
    JOIN menu_products mp ON o.menu_product_id = mp.id
    JOIN products p ON mp.product_id = p.id
    ORDER BY o.created_at ASC
    """

    orders = execute_query(query=query, fetch="all")
    if not orders:
        print("No orders found!")
        return

    for order in orders:
        print(
            f"Order ID: {order['id']}, User: {order['username']}, Product: {order['title']}, "
            f"Amount: {order['amount']}, Table number: {order['table_number']}, "
            f"Status: {order['status']}, Order type: {order['order_type']}, "
            f"Order date: {order['created_at']}"
        )


def change_order_status(order_id: int, new_status: str) -> bool:
    """Change status of order"""
    query = """
    UPDATE orders 
    SET status = %s 
    WHERE id = %s
    """
    params = (new_status, order_id)
    return execute_query(query=query, params=params)


def cancel_order(order_id: int) -> bool:
    """
    Cancels order by changing its status to 'cancelled'
    :param order_id: Order ID
    :return: bool
    """
    query = """
    UPDATE orders SET status = 'cancelled' WHERE id = %s AND status != 'cancelled'"""
    params: tuple[int] = (order_id,)
    return execute_query(query=query, params=params)

