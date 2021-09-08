from orm import session, Cookie, User, Order, LineItem, Employee
from sqlalchemy import func, cast, Numeric, and_, or_, not_

cc_cookie = Cookie(cookie_name='chocolate chip',
                   cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
                   cookie_sku='CC01',
                   quantity=12,
                   unit_cost=0.50)
session.add(cc_cookie)  #add instance to the session
session.commit()  #commit instance to the session

dcc = Cookie(cookie_name='dark chocolate chip',
             cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
             cookie_sku='CC02',
             quantity=1,
             unit_cost=0.75)
mol = Cookie(
    cookie_name='molasses',
    cookie_recipe_url='http://some.aweso.me/cookie/recipe_molasses.html',
    cookie_sku='MOL01',
    quantity=1,
    unit_cost=0.80)
session.add(dcc)  #have to add both to the session before committing
session.add(mol)
session.flush(
)  #flush is like a commit, but keeps the transaction open, and allows for two insert statements
print(dcc.cookie_id)
print(mol.cookie_id)

c1 = Cookie(cookie_name='peanut butter',
            cookie_recipe_url='http://some.aweso.me/cookie/peanut.html',
            cookie_sku='PB01',
            quantity=24,
            unit_cost=0.25)
c2 = Cookie(cookie_name='oatmeal raisin',
            cookie_recipe_url='http://some.okay.me/cookie/raisin.html',
            cookie_sku='EWW01',
            quantity=100,
            unit_cost=1.00)
session.bulk_save_objects(
    [c1, c2])  #adds multiple entries to the session in a single command
session.commit()
print(
    c1.cookie_id
)  #doesn't print anything, note that c1 and c2 are never added to the session

#this method is faster, but
#relationship settings aren't respected or triggered
#no other events are triggered
#not connected to the session (can't access them until session is restarted?)
#primary keys aren't fetched

#good for ingesting lots of data from a CSV or JSON

#updating data via the object
query = session.query(Cookie)
cc_cookie = query.filter(Cookie.cookie_name == "chocolate chip").first()
cc_cookie.quantity = cc_cookie.quantity + 120  #adding a number to the result updates the result
session.commit()  #commit the update
print(cc_cookie.quantity)  #132

#update the data in place
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "chocolate chip")
query.update({
    Cookie.quantity: Cookie.quantity - 20
})  #update method of query updates the record outside of the session
#so it doesn't need to be committed
cc_cookie = query.first()
print(cc_cookie.quantity)

#deleting data -
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "dark chocolate chip")
dcc_cookie = query.one()
session.delete(
    dcc_cookie)  #method of the session that deletes the result given a query
session.commit()
dcc_cookie = query.first()
print(dcc_cookie)

#can also be used to directly delete the results of the cookie
query = session.query(Cookie)
query = query.filter(Cookie.cookie_name == "molasses")
query.delete()

cookiemon = User(username='cookiemon',
                 email_address='mon@cookie.com',
                 phone='111-111-1111',
                 password='password')
cakeeater = User(username='cakeeater',
                 email_address='cakeeater@cake.com',
                 phone='222-222-2222',
                 password='password')
pieperson = User(username='pieperson',
                 email_address='person@pie.com',
                 phone='333-333-3333',
                 password='password')
session.add(cookiemon)
session.add(cakeeater)
session.add(pieperson)
session.flush()

#take advantage of the relationship between orders and line items when inserting in to table
#if you want to associate two tables, assign the object to the relationship property
o1 = Order()  #make a new, empty order instance
o1.user = cookiemon  #the order is from the user cookiemon (defined above)
session.add(o1)  #add the order to the session

cc = session.query(Cookie).filter(
    Cookie.cookie_name == "chocolate chip").one()  #query a cookie

line1 = LineItem(cookie=cc, quantity=2,
                 extended_cost=1.00)  #to add to an order

pb = session.query(Cookie).filter(
    Cookie.cookie_name == "peanut butter").one()  #get another cookie

line2 = LineItem(quantity=12,
                 extended_cost=3.00)  #to add to another order, this time,
line2.cookie = pb  #piece by piece
line2.order = o1  #and associate it with an order

#add orders to order object
o1.line_items.append(line1)
o1.line_items.append(line2)
session.commit()

#another order
o2 = Order()
o2.user = cakeeater
cc = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").one()
line1 = LineItem(cookie=cc, quantity=24, extended_cost=12.00)
oat = session.query(Cookie).filter(
    Cookie.cookie_name == "oatmeal raisin").one()
line2 = LineItem(cookie=oat, quantity=6, extended_cost=6.00)
o2.line_items.append(line1)
o2.line_items.append(line2)
session.add(
    o2
)  #can add it to the session whenever, as long as the object is defined and added before committing
session.commit()

#data for self-joins
# marsha = Employee(name='Marsha')
# fred = Employee(name='Fred')
# marsha.reports.append(fred)
# session.add(marsha)
# session.commit()
