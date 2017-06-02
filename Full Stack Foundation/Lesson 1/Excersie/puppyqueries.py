from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from puppies import Base, Puppy, Shelter
import datetime

engine = create_engine("sqlite:///puppyshelter.db")

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Query 1 Puppy in Ascending orders
def query_one():
	'''Query all of the puppies and return the results in ascending alphabetical order'''
	rows = session.query(Puppy.name).order_by(Puppy.name).all()
	for row in rows:
		print(row[0])

# Query 2 Puppy less than 6 months old order by younger one first
def query_two():
	'''Query all of the puppies that are less than 6 months old organized by the youngest first'''
	today = datetime.date.today()
	if passesLeapDay(today):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
	else:
		sixMonthsAgo = today - datetime.timedelta(days=182)
	rows = session.query(Puppy.name, Puppy.dateOfBirth).filter(Puppy.dateOfBirth >= sixMonthsAgo).order_by(Puppy.dateOfBirth.desc())
	for row in rows :
		print ("{name} : {dob}".format(name=row[0], dob=row[1]))

# Query 3 Weight
def query_three():
	'''Query all puppies by ascending weight'''
	rows = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight).all()
	for row in rows:
		print("{name} : {weight}".format(name=row[0], weight=row[1]))

# Query 4
def query_four():
	'''Query all puppies grouped by the shelter in which they are staying'''
	rows = session.query(Shelter, func.count(Puppy.id)).join(Puppy.shelter).group_by(Shelter.id).all()
	for row in rows:
		print (row[0].id, row[0].name, row[1])

def passesLeapDay(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    thisYear = today.timetuple()[0]
    if isLeapYear(thisYear):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
        leapDay = datetime.date(thisYear, 2, 29)
        return leapDay >= sixMonthsAgo
    else:
        return False
        
def isLeapYear(thisYear):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if thisYear % 4 != 0:
        return False
    elif thisYear % 100 != 0:
        return True
    elif thisYear % 400 != 0:
        return False
    else:
        return True

query_four()