#!/usr/bin/python3
"""
This module defines a base class for all models in the Flasheeta project.
"""

import uuid
from datetime import datetime
from flask import current_app as app

class BaseModel():
    """ 
    A base class for all Flasheeta models.

    Attributes:
        id (str): The unique identifier for the model instance.
        created_at (datetime): The timestamp when the model instance was created.
        updated_at (datetime): The timestamp when the model instance was last updated.
    """
    db = app.storage.db

    id = db.Column(db.String(60), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ 
        Instantiates a new model instance.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for key, value in kwargs.items():
                if key in ('created_at', 'updated_at'):
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)

    def to_dict(self):
        """
        Converts the instance into a dictionary format.

        Returns:
            dict: A dictionary representation of the instance.
        """
        dct = self.__dict__.copy()
        dct['created_at'] = dct.get('created_at').isoformat()
        dct['updated_at'] = dct.get('updated_at').isoformat()

        if '__class__' in dct:
            del dct['__class__']
        if '_sa_instance_state' in dct:
            del dct['_sa_instance_state']

        return dct

    def save(self):
        """
        Saves the instance in the current database session.
        """
        self.updated_at = datetime.utcnow()
        app.storage.add(self)
        app.storage.save()

    def delete(self):
        """
        Deletes the instance from the current database session.
        """
        app.storage.delete(self)
