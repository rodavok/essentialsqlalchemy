import build_db
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError

connection = build_db.engine.connect()

cookies = build_db.cookies.alias()
users = build_db.users.alias()
orders = build_db.orders.alias()
line_items = build_db.line_items.alias()

'''
# AttributeError - when you attempt to access an attribute that doesn't exist
# trying to force an attribute error:
ins = insert(build_db.users).values(
    username="cookiemon",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password"
)

result = connection.execute(ins)

s = select([users.c.username])
results = connection.execute(s)
for result in results:
    print(result.username)
    # AttributeError: Could not locate column in row for column 'password'
    print(result.password)
'''

'''
s = select([build_db.users.c.username])
connection.execute(s).fetchall()
[(u'cookiemon',)]
ins = insert(build_db.users).values(
    username="cookiemon",
    email_address="damon@cookie.com",
    phone="111-111-1111",
    password="password"
)
try:
    # IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.username
    result = connection.execute(ins)
except IntegrityError as error:
    print(error)


ins = insert(build_db.orders).values(user_id=1, order_id='1')
try:
    result = connection.execute(ins)
except IntegrityError as error:
    print(error)


ins = insert(build_db.line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 9,
        'extended_cost': 4.50
    }
]
result = connection.execute(ins, order_items)
ins = insert(build_db.orders).values(user_id=1, order_id='2')
try:
    result = connection.execute(ins)
except IntegrityError as error:
    print(error)

ins = insert(build_db.line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 4,
        'extended_cost': 1.50
    },
    {
        'order_id': 2,
        'cookie_id': 2,
        'quantity': 1,
        'extended_cost': 4.50
    }
]
try:
    result = connection.execute(ins, order_items)
except IntegrityError as error:
    print(error)

'''

'''
#Bad - creates an error if there's not enough inventory for a cookie on the order, 
#but executes the changes for cookies that can be ordered - not the desired effect

def ship_it(order_id):
    s = select([build_db.line_items.c.cookie_id,
               build_db.line_items.c.quantity])
    s = s.where(build_db.line_items.c.order_id == order_id)
    cookies_to_ship = connection.execute(s)
    for cookie in cookies_to_ship:
        u = update(build_db.cookies).where(
            build_db.cookies.c.cookie_id == cookie.cookie_id)
        u = u.values(quantity=build_db.cookies.c.quantity - cookie.quantity)
        result = connection.execute(u)
    u = update(build_db.orders).where(build_db.orders.c.order_id == order_id)
    u = u.values(shipped=True)
    result = connection.execute(u)
    print("Shipped order ID: {}".format(order_id))
'''

# ship_it(1)
# s = select([build_db.cookies.c.cookie_name, build_db.cookies.c.quantity])
# connection.execute(s).fetchall()

# ship_it(2)

'''
def ship_it(order_id):
    s = select([line_items.c.cookie_id, line_items.c.quantity])
    s = s.where(line_items.c.order_id == order_id)
    transaction = connection.begin()  # start a transaction
    cookies_to_ship = connection.execute(s).fetchall()
    #attempt to make the transaction
    try:
        for cookie in cookies_to_ship:
            u = update(cookies).where(cookies.c.cookie_id == cookie.cookie_id)
            u = u.values(quantity=cookies.c.quantity-cookie.quantity)
            result = connection.execute(u)
            u = update(orders).where(orders.c.order_id == order_id)
            u = u.values(shipped=True)
            result = connection.execute(u)
            print("Shipped order ID: {}".format(order_id))
            transaction.commit()  # commit successful transaction
    except IntegrityError as error:
        transaction.rollback()  # rollback unsuccessful transaction
        print(error)


u = update(cookies).where(cookies.c.cookie_name == "dark chocolate chip")
u = u.values(quantity=1)
result = connection.execute(u)

ship_it(2) #yields error...
s = select([cookies.c.cookie_name, cookies.c.quantity])
connection.execute(s).fetchall() # but no longer performs the transaction anyway

'''
