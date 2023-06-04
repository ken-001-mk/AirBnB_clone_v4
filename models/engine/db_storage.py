#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get_amenities_by_place(place_id):
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)


    def link_amenity_to_place(place_id, amenity_id):
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
            storage.save()
        return jsonify(amenity.to_dict()), 201


   def delete_amenity_from_place(place_id, amenity_id):
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
            place.amenities.remove(amenity)
            storage.delete(amenity)
            storage.save()
        return jsonify({}), 200


    def get(self, cls, id):
        """Retrieve one object from storage."""
        if cls in self.__session:
            objects = self.__session[cls]
            for obj_id, obj in objects.items():
                if obj_id == id:
                    return obj
        return None

    def count(self, cls=None):
        """Count the number of objects in storage."""
        if cls is None:
            return sum(len(objects) for objects in self.__session.values())
        elif cls in self.__session:
            return len(self.__session[cls])
        return 0
