#!/usr/bin/python3
""" This module defines the DBStorage class """


# from app import db
from flask_sqlalchemy import SQLAlchemy


class DBStorage():
    """ This class handles the storage of the project """

    def __init__(self, db: SQLAlchemy):
        """ """
        self.db = db

    def all(self, cls=None):
        """
        Returns the records of all cls objects or the records of all objects
        in the database if cls is None
        """
        from app.models.user import User
        from app.models.deck import Deck
        from app.models.flashcard import Flashcard
        from app.models.progress import Progress
        
        obj_dct = {}
        if cls:
            query = self.db.session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(cls.__name__, obj.id)
                obj_dct[key] = obj

        else:
            cls_lst = [User, Deck, Flashcard, Progress]
            for c in cls_lst:
                query = self.db.session.query(c).all()
                for obj in query:
                    key = "{}.{}".format(c.__name__, obj.id)
                    obj_dct[key] = obj

        return obj_dct

    def add(self, obj):
        """ adds the newly created object to the current databse session """
        if obj:
            self.db.session.add(obj)

    def save(self):
        """ Commits all changes to the current database session"""
        self.db.session.commit()

    def reload(self):
        """ Creates all tables """
        self.db.create_all()

    def delete(self, obj):
        """ Deletes obj from the current database session """
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
        
    def close(self):
        """ Closes the current database session """
        self.db.session.close()

    def get(self, cls, id):
        """  Returns the object based on the class name and its ID,
        or None if not found """
        from app.models.user import User
        from app.models.deck import Deck
        from app.models.flashcard import Flashcard
        from app.models.progress import Progress
        cls_lst = [User, Deck, Flashcard, Progress]
        if cls not in cls_lst:
            return None

        for obj in self.all().values():
            if obj.id == id:
                return obj

        return None
