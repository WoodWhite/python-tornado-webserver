# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean,\
    UniqueConstraint, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()


class People(Base):

    __tablename__ = 'people'

    id      = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name    = Column(String(128), nullable=False)
    state   = Column(String(16), nullable=False, default='Init')

    __table_args__ = (
        UniqueConstraint('name', name='peopleUnique'),
        {'mysql_engine': 'InnoDB'}
    )


def initialize(host, port, user, password, db_name, pool_size=100, pool_recycle=3600):
    DB_CONNECT = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (
        user,
        password,
        host,
        port,
        db_name
    )
    engine = create_engine(
        DB_CONNECT,
        pool_size=pool_size,
        pool_recycle=pool_recycle
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
