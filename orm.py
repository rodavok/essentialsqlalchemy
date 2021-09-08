from sqlalchemy import (Table, Column, Integer, Numeric, String, DateTime,
                        ForeignKey, Boolean, ForeignKey, create_engine)
from sqlalchemy.orm import relationship, backref, sessionmaker  #relationship and backref come from the orm portion of sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.sql.schema import CheckConstraint, ForeignKeyConstraint

Base = declarative_base()  #sqlalchemy class to inherit from
'''
Previously, tables were made using the core table instructor
when using the ORM, tables are build as classes instead
'''


#proper class to be used with the ORM must:
class Cookie(Base):  #inherit the declarative_base class
    __tablename__ = 'cookies'  #contain the name of the table in '__tablename__'

    #contain one or more columns with at least one primary key
    cookie_id = Column(Integer(), primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    #makes it easier to see and re-create object instances in core, not strictly necessary
    #print out to see how to define a new record in the table
    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
                    "cookie_recipe_url='{self.cookie_recipe_url}', " \
                    "cookie_sku='{self.cookie_sku}', " \
                    "quantity={self.quantity}, " \
                    "unit_cost={self.unit_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False,
                      unique=True)  #nullable=false - column required
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(),
                        default=datetime.now)  #defaults to current time
    updated_on = Column(
        DateTime(), default=datetime.now,
        onupdate=datetime.now)  #changes the value when a record is updated

    def __repr__(self):
        return "User(username='{self.username}', " \
            "email_address='{self.email_address}', " \
            "phone='{self.phone}', " \
            "password='{self.password}')".format(self=self)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    #foreign key defined just like in core
    #maps the orders user_id column to the users user_id column through its __tablename_
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)
    #defines a one-to-many relationship from the User class to the orders table
    #can get the user associated with the order by using the user property
    #backref establishes an orders property on the User class, allowing you to get their orders
    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return "Order(user_id={self.user_id}, " \
        "shipped={self.shipped})".format(self=self)


class LineItem(Base):
    __tablename__ = 'line_items'

    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))
    #One to many relationship from Order class to line_items table
    order = relationship("Order",
                         backref=backref('line_items', order_by=line_item_id))
    cookie = relationship('Cookie', uselist=False,
                          order_by=cookie_id)  #one-to-one relationship

    def __repr__(self):
        return "LineItems(order_id={self.order_id}, " \
        "cookie_id={self.cookie_id}, " \
        "quantity={self.quantity}, " \
        "extended_cost={self.extended_cost})".format(
        self=self)


    #the classic self-join example
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer(), primary_key=True)

    manager_id = Column(Integer(), ForeignKey('employees.id'))
    name = Column(String(255), nullable=False)

    manager = relationship(
        "Employee",  #establish a relationship between the table and itself, 
        backref=backref(
            'reports'
        ),  # where self.manager_id references self.id via the property reports
        remote_side=[id])

    def __repr__(self):
        return "Employee(id={self.id}, " \
        "manager_id={self.manager_id}, " \
        "name={self.name})".format(
        self=self)


engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

#create all of the classes inheriting base as table on the engine
Base.metadata.create_all(engine)
