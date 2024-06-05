# ORM
"""
-> class can be referenced to a whole db table
-> attributes are columns
-> a class instance can be associated with a table row
"""

import sqlite3

# create a connection to the db
conn = sqlite3.connect("restaurant.sqlite")

# in order to execute sql queries, we need a cursor
cursor = conn.cursor()

create_menus_table_sql = """
    CREATE TABLE IF NOT EXISTS menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description VARCHAR NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        preparation_time TEXT NOT NULL
    )
"""

# cursor.execute(create_menus_table_sql)

# cursor.execute("DROP TABLE menus")

class Menu:
    TABLE_NAME = "menus"

    def __init__(self, name, description, price, quantity, preparation_time):
        self.id = None
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.preparation_time = preparation_time

    # return a printable representation of the object
    def __repr__(self) -> str:
        return f"<Menu {self.id}: {self.name}, {self.description}>"

    def save(self):
        """
        the question marks are known as parameter binding which handles
        sql injections attacks
        """
        sql = f"""
            INSERT INTO {self.TABLE_NAME} (name, description, price, quantity, preparation_time)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.description, self.price,
                             self.quantity, self.preparation_time))
        conn.commit()
        self.id = cursor.lastrowid
        print(f"{self.name} created successfully")

    def update(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET name = ?, description = ?, price = ?, quantity = ?, preparation_time = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.name, self.description, self.price, self.quantity,    self.preparation_time, self.id))
        conn.commit()

    def delete(self):
        sql = f"""
            DELETE FROM {self.TABLE_NAME}
            WHERE id = ?
        """

        cursor.execute(sql, (self.id,))
        conn.commit()
        # reset the id to None
        self.id = None;

        print(f"{self.name} with id {self.id} deleted")

    @classmethod
    def create_table(cls):
        cursor.execute(create_menus_table_sql)
        print("Menus table created")
        # transaction
        conn.commit()

    @classmethod
    def drop_table(cls):
        cursor.execute("DROP TABLE IF EXISTS menus")
        conn.commit()

    @classmethod
    def alter_table(cls, type, column_name, data_type = None):
        sql = f"ALTER TABLE {cls.TABLE_NAME} DROP COLUMN {column_name}" if type == "drop" else f"ALTER TABLE {cls.TABLE_NAME} ADD COLUMN {column_name}"

        cursor.execute(sql)
        conn.commit()

# Menu.drop_table()
Menu.create_table()
# Menu.alter_table("drop", "preparation_time")

# rnb = Menu("Rice n Beans", "With Avocado", 120, 2, "40 mins")
# rnb.save()

# rice_n_stew = Menu("Rice n Stew", "With avocado", 200, 3, "1 hour")
# print(rice_n_stew)

# rice_n_stew.save()

# print(rice_n_stew)

# rice_n_stew.name = "Ugali beef"
# rice_n_stew.price = 250
# rice_n_stew.update()

# print(rice_n_stew)
