from orm_exceptions_db import User, Cookie, LineItem, Order, session
from sqlalchemy import inspect
from sqlalchemy.orm.exc import *

#create a cookie
dcc = Cookie('dark chocolate chip',
             'http://some.aweso.me/cookie/recipe_dark.html', 'CC02', 1, 0.75)
cc_cookie = Cookie('chocolate chip', 'http://some.aweso.me/cookie/recipe.html',
                   'CC01', 12, 0.50)
session.add(cc_cookie)
session.add(dcc)
session.commit()

#multipleresultsfound - the one() method is for queries that should only return one result
#results = session.query(Cookie).one()
#handled exception
try:
    results = session.query(Cookie).one()
except MultipleResultsFound as error:
    print('We found too many cookies... is that even possible?')

#detachedinstance - trying to access a relationship of an expunged object
cookiemon = User('cookiemon', 'mon@cookie.com', '111-111-1111', 'password')
session.add(cookiemon)
o1 = Order()
o1.user = cookiemon
session.add(o1)

cc = session.query(Cookie).filter(
    Cookie.cookie_name == "Change chocolate chip").one()

line1 = LineItem(order=o1, cookie=cc, quantity=2, extended_cost=1.00)

session.add(line1)
session.commit()

order = session.query(Order).first()
session.expunge(order)

try:
    results = session.query(Cookie).one()
except DetachedInstanceError as error:
    print('Object has been expunged')
'''
similar blunders include:
ObjectDeleted,
StaleData - unaccounted for DB state - garbage collected data, unsuccessful updates or deletes, refreshed objects with different numbers of rows
ConcurrentModificationError - actually just an alias of above

all relate to discrepancies b/t the objects, sessions, and the database
'''
