import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import Float

database_name = "wfh"
database_path = os.environ['DATABASE_URL']

# set in bash export DATABASE_URL = "postgres://postgres@localhost:5432/wfh"


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Walker

'''
class Walker(db.Model):  
  __tablename__ = 'walker'

  id = Column(Integer, primary_key=True)
  first_name = Column(String)
  last_name = Column(String)
  user_name = Column(String)
  age = Column(Integer)
  sex = Column(String)
  email = Column(String)
  phone = Column(String)
  area = Column(String)

  def __init__(self, first_name, last_name, user_name, age, sex, email, phone, area):
    self.first_name = first_name
    self.last_name = last_name
    self.user_name = user_name
    self.age = age
    self.sex = sex
    self.email = email
    self.phone = phone
    self.area = area

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'user_name': self.user_name,
      'age': self.age,
      'sex': self.sex,
      'email': self.email,
      'phone': self.phone,
      'area': self.area
    }

'''
Group - a group of walkers

'''
class Group(db.Model):  
  __tablename__ = 'group'

  id = Column(Integer, primary_key=True)
  group_name = Column(String)
  area = Column(String)
  no_of_members = Column(Integer)

  def __init__(self, group_name, area):
    self.group_name = group_name
    self.area = area

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'group_name': self.group_name,
      'area': self.area,
      'no_of_members': self.no_of_members
    }

'''
Event - A one time walk with a group of walkers on a route

'''
class Event(db.Model):  
  __tablename__ = 'event'

  id = Column(Integer, primary_key=True)
  route_id = Column(Integer)
  date_time = Column(String)

  def __init__(self, route_id, date_time):
    self.route_id = route_id
    self.date_time = date_time

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'route_id': self.route_id,
      'date_time': self.date_time
    }

'''
Route

'''
class Route(db.Model):  
  __tablename__ = 'route'

  id = Column(Integer, primary_key=True)
  route_name = Column(String)
  route_description = Column(String)
  route_difficulty = Column(String)
  map_link = Column(String)
  length = Column(Float)
  area = Column(String)

  def __init__(self, route_name, route_description, route_difficulty, map_link, length, area):
    self.route_name = route_name
    self.route_description = route_description
    self.route_difficulty = route_difficulty
    self.map_link = map_link
    self.length = length
    self.area = area

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'route_name': self.route_name,
      'route_description': self.route_description,
      'route_difficulty': self.route_difficulty,
      'map_link': self.map_link,
      'length': self.length,
      'area': self.area
    }