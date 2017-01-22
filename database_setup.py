import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# In order to user foreignkey relationship
from sqlalchemy.orm import relationship 

from sqlalchemy import create_engine

# Enable use of base class
Base = declarative_base()



## Classes
class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))

	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

##### import the necessary libraries, connect to restaurantMenu.db #####

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Restaurant, MenuItem
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind = engine)
# session = DBSession()

###### CREATE #####
# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# session.add(myFirstRestaurant)
# sesssion.commit()
# cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural stuff", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
# session.add(cheesepizza)
# session.commit()

##### READ #####
# firstResult = session.query(Restaurant).first()
# firstResult.name

# session.query(Restaurant).all()
# items = session.query(MenuItem).all()

# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

# for veggieBurger in veggieBurgers:
# print veggieBurger.id
# print veggieBurger.price
# print veggieBurger.restaurant.name
# print "\n"

# UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()

# for veggieBurger in veggieBurgers:
# if veggieBurger.price != '$2.99':
# veggieBurger.price = '$2.99'
# session.add(veggieBurger)
# session.commit()
