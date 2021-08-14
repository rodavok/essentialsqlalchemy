from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import select, delete, desc, cast, and_, or_, not_
# could import sum, but it conflicts with pythons sum
from sqlalchemy import func
from sqlalchemy.sql.elements import not_
import build_db

# delete functions similar to select
connection = build_db.engine.connect()

'''
s = select([build_db.cookies.c.cookie_name, build_db.cookies.c.quantity])
s = s.order_by(desc(build_db.cookies.c.quantity))
s = s.limit(2)

for cookie in rp:
    print('{} - {}'.format(cookie.quantity, cookie.cookie_name))
'''

'''
s = select([func.sum(build_db.cookies.c.quantity)])
rp = connection.execute(s)

print(rp.scalar())
'''


'''
# select count(cookie_name) from cookies
s = select([func.count(build_db.cookies.c.cookie_name).label('inventory_count')])
rp = connection.execute(s)
record = rp.first()
print(record.keys())
print(record.inventory_count)
'''

'''
# SELECT * FROM COOKIES WHERE cookie_name = 'chocolate chip'
s = select([build_db.cookies]).where(
    build_db.cookies.c.cookie_name == 'chocolate chip')
rp = connection.execute(s)
record = rp.first()
print(record.items()
'''

'''
# SELECT * FROM COOKIES WHERE cookie_name LIKE 'chocolate'
# LIKE is a 'clause', you can use any comparison like in, between, endswith, etc here
s = select([build_db.cookies]).where(
    build_db.cookies.c.cookie_name.like('%chocolate%'))
rp = connection.execute(s)
for record in rp.fetchall():
    print(record.cookie_name)
'''

'''
# string concatenation
s = select(build_db.cookies.c.cookie_name, 'SKU-' +build_db.cookies.c.cookie_sku])
for row in connection.execute(s):
    print(row)
'''


# cast converts type
# cookie quantity * unit cost - total revenue from sales (if they all sold)
# s = select([build_db.cookies.c.cookie_name,
#             cast((build_db.cookies.c.quantity * build_db.cookies.c.unit_cost),
#                  build_db.Numeric(12, 2)).label('inv_cost')])
# for row in connection.execute(s):
#     print('{} - {}'.format(row.cookie_name, row.inv_cost))

'''
SELECT * FROM cookies WHERE (and)...
s = select([build_db.cookies]).where(
    and_(
        build_db.cookies.c.quantity > 23,
        build_db.cookies.c.unit_cost < 0.40
    )
)
for row in connection.execute(s):
    print(row.cookie_name)
'''

# s = select([build_db.cookies]).where(
# or_(
# build_db.cookies.c.quantity.between(10, 50),
# build_db.cookies.c.cookie_name.contains('chip')
# )
# )
# for row in connection.execute(s):
# print(row.cookie_name)


columns = [build_db.orders.c.order_id, build_db.users.c.username, build_db.users.c.phone,
           build_db.cookies.c.cookie_name, build_db.line_items.c.quantity,
           build_db.line_items.c.extended_cost]


cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(build_db.orders.join(build_db.users).join(
    build_db.line_items).join(build_db.cookies)).where(build_db.users.c.username ==
                                                       'cookiemon')
result = connection.execute(cookiemon_orders).fetchall()
