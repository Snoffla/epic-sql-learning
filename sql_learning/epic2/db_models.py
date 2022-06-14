from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    id_number = Column(Integer, primary_key = True)
    first_name = Column(Text)
    last_name = Column(Text)
    city = Column(Text)
    state_code = Column(Text)
    shirt_or_hat = Column(Text)
    quiz_points = Column(Integer)
    team = Column(Text)
    signup = Column(Text)
    age = Column(Integer)
    company = Column(Text)

    def __repr__(self):
        return f"Person(id={self.id_number})"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class State(Base):
    __tablename__ = "states"

    state_name = Column(Text)
    state_abbrev = Column(Text, primary_key = True)
    region = Column(Text)
    division = Column(Text)

    def __repr__(self):
        return f"State(name={self.state_name}"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

engine = create_engine('sqlite:///epic2/quizdata.db', echo=True)
Session = sessionmaker(bind=engine)

def get_db_session():
    session = Session()
    return session

# for instance in session.query(Person).order_by(Person.first_name):
#     print(instance.first_name, instance.last_name)
