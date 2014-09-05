# Work-Hours.py (Version-15)

import sqlite3, sqlalchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Hours(Base):
    __tablename__ = 'hours'
    id = Column(Integer, primary_key=True)
    hours = Column(Integer, nullable=False)
    total_hours = Column(Integer)
    notes = Column(String(250))
    date = Column(DateTime, default=datetime.now)
            

engine = create_engine('sqlite:///new_work_hours.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# start session
session = Session()

class Work:
    '''Create dict to hold hours.'''
    
    total_hours = 0
    
    col_total_hours = session.query(Hours.total_hours).order_by('-id').first()
    if col_total_hours == None:
        dummy_hours = Hours(hours=0, total_hours=0, notes="dummy data")
        session.add(dummy_hours)
        session.commit()
        
    # start new session.
    session=Session()

    col_total_hours = session.query(Hours.total_hours).order_by('-id').first()
    total_hours += col_total_hours[0]
    
    def __init__(self):
        self.day = {'hours': 0}
        d = datetime.today()
        date = d.strftime("%Y-%m-%d")
        print "Your Hours For {}. . .".format(date)
        print "\n"
        

class Adjust_Hours(Work):
    '''Add or Sub hours to dict.'''
    
    def add_hours(self):
        print "Would You Like To Add Hours?"
        add = raw_input("<y> for yes, <n> for no: ")
        
        if add == "y":
            hours = input("How Many Hour(s) Would You Like To Add? ")
            self.day['hours'] += hours
            Work.total_hours += hours
            print "{} hour(s) added ".format(hours)
            print "\n"
            return
        else:
            print "No Hours To Be Added."
            print "\n"
            return
    

    def sub_hours(self):
        sub = raw_input("Would You Like To Subtract Hours? ")
        
        if sub:
            hours = input("How Many Hour(s) Would You Like To Subtract? ")
            self.day['hours'] -= hours
            Work.total_hours -= hours
            print "{} hours subtracted ".format(hours)
            print "\n"
            return
        else:
            print "No Hours To Be Subtracted.\n"
            return
        

    def add_notes(self):
        self.add_note = raw_input(str("Do You Have Any Notes For This Date? "))
        print "\n"


    def show_total_hours(self):
        current_total_hours = session.query(Hours.total_hours).order_by('-id').first()            
        print "Total Hours Before This Addition Equals {} Hours".format(current_total_hours[0])    
        new_total_hours = current_total_hours[0] + self.day['hours']                                                                                           
        print "Total Hours After This Addition Equals {}".format(new_total_hours)
        

    def save_to_db(self):
        hour = Hours(hours=self.day['hours'],total_hours=Work.total_hours, notes=self.add_note)
        session.add(hour)
        session.commit()               
        

if __name__ == '__main__':
    
    day = Adjust_Hours()
    day.add_hours()
    day.sub_hours()
    day.add_notes()
    day.show_total_hours()
    day.save_to_db()
    session.close()
    
