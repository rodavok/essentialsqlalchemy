import build_db
from sqlalchemy import insert

ins_cookies = build_db.cookies.insert()
ins_users = build_db.users.insert()

# dictionaries in list must share the same keys - so define nulls if you arent providing information for all entries.
inventory_list = [
    {
        'cookie_name': 'peanut butter',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/peanut.html',
        'cookie_sku': 'PB01',
        'quantity': '24',
        'unit_cost': '0.25'
    },
    {
        'cookie_name': 'chocolate chip',
        'cookie_recipe_url': 'http://some.aweso.me/cookie/chocochip.html',
        'cookie_sku': 'PCC01',
        'quantity': '12',
        'unit_cost': '0.50'
    },
    {
        'cookie_name': 'oatmeal raisin',
        'cookie_recipe_url': 'http://some.okay.me/cookie/raisin.html',
        'cookie_sku': 'EWW01',
        'quantity': '100',
        'unit_cost': '1.00'
    },
    {
        'cookie_name': 'dark chocolate chip',
        'cookie_recipe_url': 'http: // some.aweso.me/cookie/dark.html',
        'cookie_sku': 'CC02',
        'quantity': '1',
        'unit_cost': '0.75'
    }
]

customer_list = [
    {
        'username': 'cookiemon',
        'email_address': 'mon@cookie.com',
        'phone': '111-111-1111',
        'password': 'password'},
    {
        'username': 'cakeeater',
        'email_address': 'cakeeater@cake.com',
        'phone': '222-222-2222',
        'password': 'password'
    },
    {
        'username': 'pieguy',
        'email_address': 'guy@pie.com',
        'phone': '333-333-3333',
        'password': 'password'
    }
]


connection = build_db.engine.connect()
cookie_result = connection.execute(ins_cookies, inventory_list)
user_result = connection.execute(ins_users, customer_list)


ins = insert(build_db.orders).values(user_id=1, order_id=1)
result = connection.execute(ins)
ins = insert(build_db.line_items)
order_items = [
    {
        'order_id': 1,
        'cookie_id': 1,
        'quantity': 2,
        'extended_cost': 1.00
    },
    {
        'order_id': 1,
        'cookie_id': 3,
        'quantity': 12,
        'extended_cost': 3.00
    }
]
result = connection.execute(ins, order_items)
ins = insert(build_db.orders).values(user_id=2, order_id=2)
result = connection.execute(ins)
ins = insert(build_db.line_items)
order_items = [
    {
        'order_id': 2,
        'cookie_id': 1,
        'quantity': 24,
        'extended_cost': 12.00
    },
    {
        'order_id': 2,
        'cookie_id': 4,
        'quantity': 6,
        'extended_cost': 6.00
    }
]
result = connection.execute(ins, order_items)
