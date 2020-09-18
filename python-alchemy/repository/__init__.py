from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ENGINE:
    SQLITE = "sqlite:///user.db"
    MYSQL = "mysql+mysqldb://admin:admin@localhost:3306/users_db"


engine = create_engine(ENGINE.MYSQL)


def get_session():
    sqlite_engine = engine
    Session = sessionmaker(bind=sqlite_engine)
    session = Session()
    return session


'''
declarative_base() is a factory function that constructs a base class 
for declarative class definitions
'''
Base = declarative_base()


def create_all():
    Base.metadata.create_all(engine)


