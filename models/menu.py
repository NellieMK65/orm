from datetime import datetime
from db import conn, cursor

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
        return f"<Menu {self.id}: {self.name}, {self.description}, {self.price}, {self.quantity}, {self.preparation_time}>"

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

    def soft_delete(self):
        sql = f"""
            UPDATE {self.TABLE_NAME}
            SET deleted_at = ?
            WHERE id = ?
        """
        cursor.execute(sql, (datetime.now(), self.id))
        conn.commit()

        print(f"{self.name} with id {self.id} soft deleted")

    @classmethod
    def find_one(cls, id):
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE id = ?
        """
        row = cursor.execute(sql, (id,)).fetchone()

        if row == None:
            return None

        return cls.row_to_instance(row)

    @classmethod
    def find_all(cls, deleted = False):
        where_clause = "IS NOT NULL" if deleted else "IS NULL"
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME}
            WHERE deleted_at {where_clause}
        """

        rows = cursor.execute(sql).fetchall()

        return [cls.row_to_instance(row) for row in rows]

    @classmethod
    def row_to_instance(cls, row):
        menu = cls(row[1], row[2], row[3], row[4], row[5])
        menu.id = row[0]

        return menu


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
        sql = f"ALTER TABLE {cls.TABLE_NAME} DROP COLUMN {column_name}" if type == "drop" else f"ALTER TABLE {cls.TABLE_NAME} ADD COLUMN {column_name} {data_type}"

        cursor.execute(sql)
        conn.commit()

# Menu.drop_table()
Menu.create_table()
