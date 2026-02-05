"""
    Tables:
    users: id, username, password, is_login, created_at
    products: id, title, price, description, created_at
    menu_products: id, date_of_menu, product_id, amount, created_at
    durations: id, from_time, to_time, seats, created_at
    orders: id, user_id, menu_product_id, amount, duration_id, status, order_type, created_at
"""


users = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_login BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """

products = """
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price BIGINT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """

menu_products = """
CREATE TABLE menu_products (
    id SERIAL PRIMARY KEY,
    dete_of_menu DATE DEFAULT CURRENT_DATE, -- Python kodingizdagi 'dete' so'zi bilan moslandi
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """

durations="""
CREATE TABLE durations (
    id SERIAL PRIMARY KEY,
    from_time TIME NOT NULL,
    to_time TIME NOT NULL,
    seats INT DEFAULT 50, -- Har bir vaqt oralig'i uchun 50 ta joy
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """


orders = """
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    menu_product_id INT REFERENCES menu_products(id),
    amount INT NOT NULL,
    duration_id INT REFERENCES durations(id),
    table_number INT NOT NULL, -- Stol raqami kerak
    status VARCHAR(50) DEFAULT 'pending',
    order_type VARCHAR(255),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Main kodidatgi 'create_at' bilan moslandi
);
        """

