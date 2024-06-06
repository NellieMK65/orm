# ORM
"""
-> class can be referenced to a whole db table
-> attributes are columns
-> a class instance can be associated with a table row
"""
from models.menu import Menu
from models.customer import Customer
from models.order import Order

menus = Menu.find_all(deleted=False)
# print(menus)

customer_1 = Customer("Leslie", "0712345678")
# customer_1.save()

print(customer_1)

customer_2 = Customer.find_one(2)
customer_2_orders = customer_2.orders()

print(customer_2_orders)

order_1 = Order(customer_2.id, 1000)
# order_1.save()
order_2 = Order(customer_2.id, 400)
# order_2.save()
