#!/usr/bin/python3

from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import Base



class DBStorage:
    """This class is the link between objects and the database"""
    __engine = None
    __session = None
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    def __init__(self):
        """ Initialization of Database """
        self.user = getenv('HBNB_MYSQL_USER')
        self.pwd = getenv('HBNB_MYSQL_PWD')
        self.host = getenv('HBNB_MYSQL_HOST')
        self.db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(self.user, self.pwd,
                                             self.host, self.db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Sqlalchemy query that returns appropriate data"""
        objects = {}

        if cls is None:
            for class_name in self.classes:
                type_of_class = eval(class_name)
                for value in self.__session.query(type_of_class).all():
                    key = "{}.{}".format(type_of_class.__name__, value.id)
                    objects[key] = value
            return objects
        for value in self.__session.query(cls).all():
            key = "{}.{}".format(cls.__name__, value.id)
            objects[key] = value

        return objects


    def new(self, obj):
        """ Function that inserts object as row into database"""
        self.__session.add(obj)

    def save(self):
        """ Function that commits all changes/new rows"""
        self.__session.commit()

    def delete(self, obj=None):
        """ Function that deletes object from current session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Function that creates table in database """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
