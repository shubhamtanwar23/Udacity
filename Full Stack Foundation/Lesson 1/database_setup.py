import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Begin
Base = declarative_base()

class Restaurant(Base):
	"""Class for Table restaurant in Database via orm"""
	# Table Name
	__tablename__ = 'restaurant'
	
	# name column
	name = Column(String(80), nullable=False)

	# id column
	id = Column(Integer, primary_key=True)



class MenuItem(Base):
	"""Class for Table menu_item in Database via orm"""

	# Table menu_item
	__tablename__ = 'menu_item'

	# name column
	name = Column(String(80), nullable=False)

	# id column
	id = Column(Integer, primary_key=True)

	# course column
	course = Column(String(250))

	# description column
	description = Column(String(250))

	# price column
	price = Column(String(8))

	# restaurant_id column 
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

	# restaurant relationship
	restaurant = relationship(Restaurant)



# End of file
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)