#!/usr/bin/python
""" This module defines a base class for all models in the Flasheeta project """


import uuid
from datetime import datetime
from flask import current_app as app 

class BaseModel():
     """ A base class for all Flasheeta models """
     from app import db
     id = db.Column(db.String(60), nullable=False, primary_key=True)
     created_at = db.Column(
          db.DateTime,
    nullable=False,
     default=datetime.utcnow)

     updated_at = db.Column(
    db.DateTime,
    nullable=False,
     default=datetime.utcnow)

     def __init__(self, *args, **kwargs):
          """ Instatntiates a new model """
          self.id = str(uuid.uuid4())
          self.created_at = datetime.utcnow()
          self.updated_at = datetime.utcnow()

          if kwargs:
               for key, value in kwargs.items():
                    if key == 'created_at' or key == 'updated_at':
                         value = datetime.strptime(kwargs.get(key),
                                                   '%Y-%m-%dT%H:%M:%S.%f')
                    if key != '__class__':
                         setattr(self, key, value)

     def to_dict(self):
          """ Converts instance into dict format """
          dct = self.__dict__
          if '__class__' in dct:
               del dct['__class__']
               dct['created_at'] = dct.get('created_at').isoformat()
               dct['updated_at'] = dct.get('updated_at').isoformat()

          if '_sa_instance_state' in dct:
               del dct['_sa_instance_state']

          return dct

     def save(self):
          """ Saves the instance in the currenct database Session """
          self.updated_at = datetime.utcnow()
          #Adds the new object to the database
          app.storage.add(self)
          app.storage.save()

     def delete(self):
          """ Deletes the instance from the current database session """
          app.storage.delete(self)
