from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
Base = declarative_base()

#ADD YOUR USER MODEL HERE
class User(Base):
	"""docstring for User"""
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String(32))
	password = Column(String(64))

	def hash_password(self, passwd):
		self.password = pwd_context.encrypt(passwd)

	def verify_password(self, passwd):
		return pwd_context.verify(passwd, self.password)


class Bagel(Base):
	__tablename__ = 'bagel'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	picture = Column(String)
	description = Column(String)
	price = Column(String)
	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	    'name' : self.name,
	    'picture' : self.picture,
	    'description' : self.description,
	    'price' : self.price
	        }


engine = create_engine('sqlite:///bagelShop.db')
 

Base.metadata.create_all(engine)