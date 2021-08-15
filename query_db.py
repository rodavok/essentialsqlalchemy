from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import select, delete, desc, cast, and_, or_, not_
# could import sum, but it conflicts with pythons sum
from sqlalchemy import func
from sqlalchemy.sql.elements import not_
import build_db

# delete functions similar to select
connection = build_db.engine.connect()

cookies = build_db.cookies.alias()
users = build_db.users.alias()
orders = build_db.orders.alias()
line_items = build_db.line_items.alias()

'''
s = select([cookies.c.cookie_name, cookies.c.quantity])
s = s.order_by(desc(cookies.c.quantity))
s = s.limit(2)

for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))
'''

'''
s = select([func.sum(cookies.c.quantity)])
rp = connection.execute(s)

print(rp.scalar())
'''


'''
# select count(cookie_name) from cookies
s = select([func.count(cookies.c.cookie_name).label('inventory_count')])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)
'''

'''
# SELECT * FROM COOKIES WHERE cookie_name = 'chocolate chip'
s = select([cookies]).where(
    cookies.c.cookie_name == 'chocolate chip')
rp = connection.execute(s)
record = rp.first()
print(record.items()
'''

'''
# SELECT * FROM COOKIES WHERE cookie_name LIKE 'chocolate'
# LIKE is a 'clause', you can use any comparison like in, between, endswith, etc here
s = select([cookies]).where(
    cookies.c.cookie_name.like('%chocolate%'))
rp = connection.execute(s)
for record in rp.fetchall():
    print(record.cookie_name)
'''

'''
# string concatenation
s = select(cookies.c.cookie_name, 'SKU-' +cookies.c.cookie_sku])
for row in connection.execute(s):
    print(row)
'''


# cast converts type
# cookie quantity * unit cost - total revenue from sales (if they all sold)
# s = select([cookies.c.cookie_name,
#             cast((cookies.c.quantity * cookies.c.unit_cost),
#                  Numeric(12, 2)).label('inv_cost')])
# for row in connection.execute(s):
#     print('{} - {}'.format(row.cookie_name, row.inv_cost))

'''
SELECT * FROM cookies WHERE (and)...
s = select([cookies]).where(
    and_(
        cookies.c.quantity > 23,
        cookies.c.unit_cost < 0.40
    )
)
for row in connection.execute(s):
    print(row.cookie_name)
'''

# s = select([cookies]).where(
# or_(
# cookies.c.quantity.between(10, 50),
# cookies.c.cookie_name.contains('chip')
# )
# )
# for row in connection.execute(s):
# print(row.cookie_name)

'''
#SELECT o.order_id, u.username, u.phone, c.cookie_name, l.quantity, l.extended_cost
#FROM orders o
#JOIN users u ON u.user_id = o.user_id
#JOIN line_items l ON o.order_id = l.order_id
#JOIN cookies c ON l.cookie_id = c.cookie_id
#WHERE u.username = 'cookiemon';

columns = [orders.c.order_id, users.c.username, users.c.phone,
           cookies.c.cookie_name, line_items.c.quantity,
           line_items.c.extended_cost]

select object has method select_from, which allows you to specify a FROM clause for things like joins

cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(orders.join(users).join(
    line_items).join(cookies)).where(users.c.username ==
                                                       'cookiemon')
result = connection.execute(cookiemon_orders).fetchall()
'''
'''
#SELECT u.username, count(o.order_id)
#FROM users u
#OUTER JOIN orders o
#ON u.user_id = o.user_id
#GROUP BY u.username
columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
#Using outerjoin method from users will include users that don't have any orders
all_orders = all_orders.select_from(users.outerjoin(orders))
all_orders = all_orders.group_by(users.c.username)
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)
'''

'''
#use function parameters to create modifiers for your queries
def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [orders.c.order_id, users.c.username, users.c.phone]
    joins = users.join(orders)
    if details:
        columns.extend([cookies.c.cookie_name, line_items.c.quantity,
                        line_items.c.extended_cost])
    joins = joins.join(line_items).join(cookies)
    cust_orders = select(columns)
    cust_orders = cust_orders.select_from(joins)
    cust_orders = cust_orders.where(users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(orders.c.shipped == shipped)
    result = connection.execute(cust_orders).fetchall()
    return result
'''

'''
#can simply execute raw queries via execute, but can cause security issues
result = connection.execute("select * from orders").fetchall()
print(result)
'''
