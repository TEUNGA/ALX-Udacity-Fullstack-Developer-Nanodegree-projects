#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey


# TODO: connect to a local postgresql database
# connecting to local postgresql
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# connecting to local postgresql
def fyyur_db(app):
    db.app = app
    db.init_app(app)
    return db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    
    seeking_talent = db.Column(Boolean, default=False)
    
    genres = db.Column(ARRAY(String))
    seeking_description = db.Column(db.String(500), default='')
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    website_link = db.Column(String(120))

    def __init__(self, genres, address, city, state, name, phone, website_link, facebook_link, image_link,
                 seeking_talent=False, seeking_description=""):
        self.name = name
        self.genres = genres
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.website_link = website_link
        self.seeking_description = seeking_description
        self.image_link = image_link
        self.facebook_link = facebook_link
       

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    def short(self):
        return{
            'id':self.id,
            'name':self.name,
        }
    
    def long(self):
        print(self)
        return{
            'id' :self.id,
            'state' :self.state,
             'name' :self.name,
            'city' : self.city,
        }
    
    def detail(self):
        return{
            'id' :self.id,
            'address' :self.address,
            'name' :self.name,
            'genres' : self.genres,
            'website_link' :self.website_link,
            'facebook_link':self.facebook_link,
            'seeking_talent' :self.seeking_talent,
            'seeking_description' :self.seeking_description,
            'image_link' :self.image_link,
            'city' :self.city,
            'state' :self.state,
            'phone' :self.phone
           
        }

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default=' ')
    website_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    def __init__(self, name, genres, city, state, phone, image_link, website_link, facebook_link,
                    seeking_venue=False,seeking_description=""):
            self.name = name
            self.website_link = website_link
            self.facebook_link = facebook_link
            self.seeking_description =seeking_description
            self.genres = genres
            self.city = city
            self.state = state
            self.phone = phone
            self.image_link = image_link
        
    def insert(self):
                db.session.add(self)
                db.session.commit()
            
    def update(self):
                db.session.commit()
            
    def short(self):
                return{
                    'id': self.id,
                    'name':self.name,
                }
            
    def details(self):
                return{
                    'id': self.id,
                    'name': self.name,
                    'genres': self.genres,
                    'city': self.city,
                    'state':self.state,
                    'phone': self.phone,
                    'seeking_venue': self.seeking_venue,
                    'seeking_description': self.seeking_description,
                    'image_link': self.image_link,
                    'website_link': self.website_link,
                    'facebook_link': self.facebook_link,

                }



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# implementing the show model
class Show(db.Model):

    __tablename__ = 'Show'
    id = db.Column(Integer,primary_key=True)
    venue_id = db.Column(Integer, ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(Integer, ForeignKey(Artist.id), nullable=False)
    start_time = db.Column(String(), nullable=False)


    def __init__(self, venue_id,artist_id,start_time):
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def detail(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name' :self.Venue.name,
            'artist_id' :self.artist_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time
        }

    def artist_details(self):
        return{
            'artist_id' :self.venue_id,
            'artist_name' :self.Artist.name,
            'artist_image_link' :self.Artist.image_link,
            'start_time' :self.start_time

        }
 
    
    def venue_details(self):
        return{
            'venue_id' :self.venue_id,
            'venue_name':self.Venue.name,
            'venue_image_link' :self.Venue.image_link,
            'start_time' :self.start_time
            
        }