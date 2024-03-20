#!/usr/bin/python3
"""DB Storage"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review


class DBStorage():
    """Our DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate the class."""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")
            ),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session all objects,
        depending of the class name (argument cls).
        """
        all_classes = [City, State, User, Place, Review, Amenity]
        output = {}
        if cls:
            for obj in self.__session.query(cls).all():
                output[f'{obj.__class__.__name__}.{obj.id}'] = obj
        else:
            for cls in all_classes:
                for obj in self.__session.query(cls).all():
                    output[f'{obj.__class__.__name__}.{obj.id}'] = obj
        return output

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """ calls close() method on Session class with curr session as arg """
        self.__session.__class__.close(self.__session)