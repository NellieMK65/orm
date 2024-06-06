from collections import defaultdict

from db import conn, cursor
from models.order import Order

customer_dict = defaultdict(lambda: Customer(name=None, phone=None))

class Customer:
    TABLE_NAME = "customers"

    def __init__(self, name, phone):
        self.id = None
        self.name = name
        self.phone = phone
        self.created_at = None
        self.orders = []

    def __repr__(self) -> str:
        return f"<Customer {self.id}, {self.name}, {self.phone}, {self.created_at}, {self.orders}>"

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, phone)
            VALUES (?, ?)
        """

        cursor.execute(sql, (self.name, self.phone))
        conn.commit()

        self.id = cursor.lastrowid
        print(f"{self.name} created successfully")

    def my_orders(self):
        sql = f"""
            SELECT * FROM orders
            WHERE customer_id = ?
        """

        rows = cursor.execute(sql, (self.id,)).fetchall()

        return [
            Order.row_to_instance(row) for row in rows
        ]

    def get_orders(self):
        sql = """
            SELECT customers.*, orders.id, orders.total, orders.created_at FROM customers
            LEFT JOIN orders ON customers.id = orders.customer_id
            WHERE customers.id = ?
        """

        rows = cursor.execute(sql, (self.id,)).fetchall()

        for row in rows:
            customer_id = row[0]
            customer_name = row[1]
            customer_phone = row[2]
            customer_created_at = row[3]
            order_id = row[4]
            order_total = row[5]
            order_created_at = row[6]

            if customer_dict[customer_id].id is None:
                customer_dict[customer_id].id = customer_id
                customer_dict[customer_id].name = customer_name
                customer_dict[customer_id].phone = customer_phone
                customer_dict[customer_id].created_at = customer_created_at

            if order_id is not None:
                order = Order(customer_id, order_total)
                order.id = order_id
                order.created_at = order_created_at
                customer_dict[customer_id].orders.append(order.to_dict())

        return customer_dict.get(customer_id).to_dict()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "created_at": self.created_at,
            "orders": self.orders
        }

    @classmethod
    def find_one(cls, id):
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE id = ?
        """
        row = cursor.execute(sql, (id,)).fetchone()

        return cls.row_to_instance(row)

    @classmethod
    def row_to_instance(cls, row):
        if row == None:
            return None

        customer = cls(row[1], row[2])
        customer.id = row[0]
        customer.created_at = row[3]

        return customer

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        cursor.execute(sql)
        conn.commit()
        print("Customers table created")

    # we no longer need this
    @classmethod
    def make_phone_unique(cls):
        cursor.execute("CREATE UNIQUE INDEX unique_customers_phone ON customers (phone)")
        conn.commit()

Customer.create_table()
# Customer.make_phone_unique()
