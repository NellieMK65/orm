from db import conn, cursor

class Order:
    TABLE_NAME = "orders"

    def __init__(self, customer_id, total) -> None:
        self.id = None
        self.customer_id = customer_id
        self.total = total
        self.created_at = None

    def __repr__(self) -> str:
        return f"<Order {self.id}, Customer Id: {self.customer_id}, {self.total}, {self.created_at}>"

    def save(self):
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (customer_id, total)
            VALUES (?, ?)
        """

        cursor.execute(sql, (self.customer_id, self.total))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def row_to_instance(cls, row):
        if row == None:
            return None

        order = cls(row[1], row[2])
        order.id = row[0]
        order.created_at = row[3]

        return order

    @classmethod
    def create_table(cls):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL REFERENCES customers(id),
                total INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(sql)
        conn.commit()
        print("Orders table created")

Order.create_table()
