#!/usr/bin/python3
""" This module defines the DBStorage class """


from flask_sqlalchemy import SQLAlchemy

class DBStorage():
    """
    This class handles the storage operations for the project's database.

    Methods:
        __init__(self, db: SQLAlchemy): Initializes a new database storage instance.
        add(self, obj): Adds a new object to the current database session.
        save(self): Commits all changes to the current database session.
        delete(self, obj): Deletes an object from the current database session.
        close(self): Closes the current database session.
        get(self, cls, id): Retrieves an object from the database based on its class and ID.
    """

    def __init__(self, db: SQLAlchemy):
        """
        Initializes a new database storage instance.

        Args:
            db (SQLAlchemy): The SQLAlchemy instance to use for database operations.
        """
        self.db = db


    def all(self, cls=None):
        """
        Returns records of all objects of a specified class or all objects in the database if cls is None.

        Args:
            cls (class, optional): The class of objects to retrieve records for. Defaults to None.

        Returns:
            dict: A dictionary mapping object keys to their corresponding objects.
                  The key format is "{Class Name}.{object.id}".
        """
        from app.models.user import User
        from app.models.deck import Deck
        from app.models.flashcard import Flashcard
        from app.models.progress import Progress

        obj_dict = {}

        if cls:
            query = self.db.session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(cls.__name__, obj.id)
                obj_dict[key] = obj
        else:
            cls_list = [User, Deck, Flashcard, Progress]
            for c in cls_list:
                query = self.db.session.query(c).all()
                for obj in query:
                    key = "{}.{}".format(c.__name__, obj.id)
                    obj_dict[key] = obj

        return obj_dict


    def add(self, obj):
        """
        Adds a new object to the current database session.

        Args:
            obj: The object to be added to the database session.
        """
        if obj:
            self.db.session.add(obj)

    def save(self):
        """ Commits all changes to the current database session"""
        self.db.session.commit()

    def delete(self, obj):
        """
        Deletes an object from the current database session.

        Args:
            obj: The object to be deleted from the database session.
        """
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()

    def close(self):
        """ Closes the current database session """
        self.db.session.close()

    def get(self, cls, id):
        """
        Retrieves an object from the database based on its class and ID.

        Args:
            cls: The class of the object to retrieve.
            id: The ID of the object to retrieve.

        Returns:
            object: The retrieved object if found, otherwise None.
        """
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
