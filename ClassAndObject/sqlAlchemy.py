
from sqlalchemy import Column,String,create_engine
from sqlalchemy.orm import sessionmaker,relationships
from sqlalchemy.ext.declarative import declarative_base
import pymysql

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'0
    id = Column(String(20),primary_key=True)
    name = Column(String(20))
    books = relationships('Book')


class Book(Base):
    __tablename__ = 'book'
    id = Column(String(20),primary_key=True)
    name = Column(String(20))


class School(Base):
    __tablename__ = 'school'
    id = Column(String(20),primary_key=True)
    name = Column(String(20))


if __name__ == '__main__':
    sql_connect_string = "mysql+pymysql://root:123456@localhost:3306/yk?charset=utf8"
    engine = create_engine(sql_connect_string,encoding='utf-8')
    DBSession = sessionmaker(bind=engine)
    session =DBSession()
    # new_user = User(id='3',name='hill')
    # new_school = School(id='1',name='洛阳一中')
    # session.add(new_user)
    # session.add(new_school)
    user = session.query(User).filter(User.id=='1').one()
    print(type(user))
    print(user)
    # session.commit()
    # session.close()