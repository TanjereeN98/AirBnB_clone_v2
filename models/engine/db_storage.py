#!/usr/bin/python3
"""This module defines a class to manage DBStorage for hbnb clone"""

from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base


class DBStorage:
    """This class manages DBstorage of hbnb clone"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiation of the DBStorage"""

        dialect = 'mysql'
        driver = 'mysqldb'
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('{}+{}://{}:{}@{}/{}'.
                                      format(dialect, driver, HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD, HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        all objects depending of the class name
        """
        dict = {}
        classes = [City, State, User, Place, Review, Amenity]
        if cls:
            for obj in self.__session.query(cls).all():
                dict[f'{obj.__class__.__name__}.{obj.id}'] = obj
        else:
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    dict[f'{obj.__class__.__name__}.{obj.id}'] = obj
        return dict

    def new(self, obj):
        """Adds new object to DBStorage dictionary"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads objects and prepare the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
