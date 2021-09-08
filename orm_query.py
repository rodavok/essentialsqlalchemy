from orm import session, Cookie, User, Order, LineItem, Employee
from sqlalchemy import func, cast, Numeric, and_, or_, not_, text

cookies = session.query(Cookie).all()
print(cookies)
#prints a list of orm.Cookie objects

for cookie in session.query(Cookie):
    print(cookie)
#iterates over cookie and prints one of each object
# more efficient than handling a full list, and you ususally use one record at a time anyway
# query().first() to pull first result, .one() to ensure your query only pulled one
# .scalar() expects the query to return a single row with a single column - tricky to use

#limiting queries - columns
print(session.query(Cookie.cookie_name, Cookie.quantity).first()
      )  #select only cookie name and quantity, and returns the first result

#order ascending by cookie quantity
for cookie in session.query(Cookie).order_by(Cookie.quantity):
    print('{:3} - {}'.format(cookie.quantity, cookie.cookie_name))

#limiting to 2 with array slicing
#.first() returns the first result of a query, but actually pulls the whole query
#array slicing actually limits the results of the query
query = session.query(Cookie).order_by(
    Cookie.quantity)[:2]  #can also use .limit(2)
print([result.cookie_name for result in query])

#can use SQL functions via func as well
#don't import sum from sqlalchemy.func, as it causes problems with python's sum
inv_count = session.query(func.sum(
    Cookie.quantity)).scalar()  #scalar returns a single value
print(inv_count)  #138 total cookies

rec_count = session.query(func.count(
    Cookie.cookie_name)).first()  #first returns a tuple
print(rec_count)

# the varying return is not good, and it also gives automatically generated column names (not good)
#  we can fix it with label()
rec_count = session.query(func.count(Cookie.cookie_name) \
                                    .label('inventory_count')).first()
print(rec_count.keys())
print(rec_count.inventory_count)

#filtering is like where
#filter by cookie name
record = session.query(Cookie).filter(
    Cookie.cookie_name == 'chocolate chip').first()
print(record)

#filter_by is slightly cleaner and more implicit, filters using an attribute of the primary entity or the last that was joined to the statement
record = session.query(Cookie).filter_by(cookie_name='chocolate chip').first()
print(record)

#filter using 'like'
query = session.query(Cookie).filter(Cookie.cookie_name.like('%chocolate%'))
for record in query:
    print(record.cookie_name)

##operators
# ==, !=, <, etc work in sqla as in python
#sring concatenation with +
#== None is equivalent to IS NULL - i'll need to remember this someday (hopefully)
results = session.query(Cookie.cookie_name, 'SKU-' + Cookie.cookie_sku).all()
for row in results:
    print(row)

#cast allows type conversions
#here, cookie quantity * cost would produce an ugly number with many trailing 0s,
#and cast makes it look like currency
query = session.query(
    Cookie.cookie_name,
    cast((Cookie.quantity * Cookie.unit_cost), Numeric(12,
                                                       2)).label('inv_cost'))

for result in query:
    print('{} - {}'.format(result.cookie_name, result.inv_cost))

#instead of chaining multiple filters, use conjuctions
#and_(), or_(), and not_()
#filters cookies with quantity over 23, and cheaper than .40c each
query = session.query(Cookie).filter(Cookie.quantity > 23,
                                     Cookie.unit_cost < 0.40)
for result in query:
    print(result.cookie_name)

#cookies with quantities between 10 and 50, or those that have chip in the name
query = session.query(Cookie).filter(
    or_(Cookie.quantity.between(10, 50), Cookie.cookie_name.contains('chip')))
for result in query:
    print(result.cookie_name)

#querying joins to select from multiple tables

query = session.query(
    Order.order_id,
    User.username,
    User.phone,  #SELECT FROM
    Cookie.cookie_name,
    LineItem.quantity,
    LineItem.extended_cost)
query.join(User).join(LineItem).join(Cookie)  #JOIN
results = query.filter(User.username == 'cookiemon').all(
)  #get information about user cookiemon across three different tables
print(results)

#outer join to get all users and their order numbers, even if they don't have any
query = session.query(User.username, func.count(
    Order.order_id))  #select username, count(order_id)
query = query.outerjoin(Order).group_by(User.username)
#FROM Order, User
#OUTER JOIN on user_id
#GROUP BY User.username
for row in query:
    print(row)
'''
marsha = Employee(name='Marsha')
fred = Employee(name='Fred')
marsha.reports.append(fred)
session.add(marsha)
session.commit()
for report in marsha.reports:
    print(report.name) #marsha reports to fred, another employee
'''

#grouping - as usual, you need column(s) to group on and columns(s) to aggregate
query = session.query(User.username, func.count(
    Order.order_id))  #Select u.username, COUNT(o.order_id)
query = query.outerjoin(Order).group_by(
    User.username)  #FROM Order JOIN User ON user_id GROUPBY username
for row in query:
    print(row)


#Query Chaining
#wrap a previous query in a function
def get_orders_by_customer(cust_name):
    query = session.query(Order.order_id, User.username, User.phone,
                          Cookie.cookie_name, LineItem.quantity,
                          LineItem.extended_cost)
    query = query.join(User).join(LineItem).join(Cookie)
    results = query.filter(User.username == cust_name).all()
    return results


get_orders_by_customer('cakeeater')

#but what if you wanted only orders that had or hadn't been shipped yet?
#or if you didn't want Ally the details?


#add params to the function
#and use control structures to build the query
def get_orders_by_customer(cust_name, shipped=None, details=False):
    #base columns to return
    query = session.query(Order.order_id, User.username, User.phone)
    #join on initial tables involved
    query = query.join(User)
    if details:
        #superfluous data to include if asked for
        #
        query = query.add_columns(Cookie.cookie_name, LineItem.quantity,
                                  LineItem.extended_cost)
        #join on the new tables referenced
        query = query.join(LineItem).join(Cookie)
    if shipped is not None:
        #add a clause to filter only orders that have been shipped or not shipped specified
        query = query.where(Order.shipped == shipped)
    results = query.filter(User.username == cust_name).all()
    return results


#get additional info about the orders for user that have not been shipped
get_orders_by_customer('cakeeater', shipped=False, details=True)

#Raw queries
#you can just use SQL for portions of a query
query = session.query(User).filter(text("username='cookiemon'"))
print(query.all())
