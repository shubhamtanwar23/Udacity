# Using Database via ORM

### Creating Database via SQLAlchemy

* First import these python modules
```sh
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
```

  1. Configuration :- Connecting to database and SQL engine.
  Code for configuration
  ```sh
  # Beginning of file
  Base = declarative_base()
  #
  # Class declarations ...
  #
  # End of file
  engine = create_engine('sqlite:///restaurantmenu.db')
  Base.metadata.create_all(engine)
  
  2. Class :- Representation of Table as a class. Must inherit from Base class of SQLAlchemy
  ```sh
  class Restaurant(Base):
  ```
  
  3. Table :- Representation of table inside the database.
  ```sh
  # Table Name
  __tablename__ = 'restaurant'
  ```
  
  4. Mapper :- Mapping columns and objects
  ```sh
  # Object to Column Mapper
  name = Column(String(80), nullable=False)
  ```
  
### Session for Query Generation

For using the database we first need to make a session for generating query
```sh
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()
```
### Insert Query
To insert data in table we just need to create an object of the table class. After that add that object into session and 
call commit() to perform changes in database.
```sh
myFirstRestaurant = Restaurant(name='Pizza Palace')
session.add(myFirstRestaurant)
session.commit()
```
### Select Query 
To read rows call query() of session with Columns you want to read as its parameters
```sh
rows = session.query(Restaurant).all()
```
### Update Query 
To update rows first retrieve the object of row you want to change and then change its value
and then perform commit
```sh
Pizza = session.query(Restaurant).filter_by(Restaurant.name == 'Pizza Palace').one()
Pizza.name = 'Burger Palace'
session.add(Pizza)
session.commit()
```

### Delete Query 
To delete rows first retrieve the object of row you want to delete and call delete() with 
object as parameter and peroform commit
```sh
Burger = session.query(Restaurant).filter_by(Restaurant.name == 'Burger Palace').one()
session.delete(Burger)
session.commit()
```


