#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

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
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

def fyyur_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
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

    
    search_talent = db.Column(Boolean, default=False)
    
    genres = db.Column(ARRAY(String))
    description = db.Column(db.String(500), default='')
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    web_site = db.Column(String(120))

    def __init__(name, genres, address, city, state,uniq, phone, web_site, facebook_link, image_link,
                 search_talent=False, description=""):
        uniq.name = name
        uniq.genres = genres
        uniq.address = address
        uniq.city = city
        uniq.state = state
        uniq.phone = phone
        uniq.web_site = web_site
        uniq.description = description
        uniq.image_link = image_link
        uniq.facebook_link = facebook_link
       

    def insert(uniq):
        db.session.add(uniq)
        db.session.commit()

    def update(uniq):
        db.session.commit()
    
    def delete(uniq):
        db.session.delete(uniq)
        db.session.commit()
  
    def short(uniq):
        return{
            'id':uniq.id,
            'name':uniq.name,
        }
    
    def long(uniq):
        print(uniq)
        return{
            'id' :uniq.id,
            'state' :uniq.state,
             'name' :uniq.name,
            'city' : uniq.city,
        }
    
    def detail(uniq):
        return{
            'id' :uniq.id,
            'address' :uniq.address,
            'name' :uniq.name,
            'genres' : uniq.genres,
             'web_site' :uniq.web_site,
            'facebook_link':uniq.facebook_link,
            'search_talent' :uniq.search_talent,
            'description' :uniq.description,
            'image-link' :uniq.image_link,
            'city' :uniq.city,
            'phone' :uniq.phone
           
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

    search_venue = db.Column(db.Boolean, default=False)
    search_description = db.Column(db.String(120), default=' ')
    web_site = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


def __init__(uniq, name, genres, city, state, phone, image_link, web_site, facebook_link,
                search_venue=False,search_description=""):
        uniq.name = name
        uniq.web_site = web_site
        uniq.facebook_link = facebook_link
        uniq.search_description =search_description
        uniq.genres = genres
        uniq.city = city
        uniq.state = state
        uniq.phone = phone
        uniq.image_link = image_link
    
        def insert(uniq):
            db.session.add(uniq)
            db.session.commit()
        
        def update(uniq):
            db.session.commit()
        
        def short(uniq):
            return{
                'id': uniq.id,
                'name':uniq.name,
            }
        
        def details(uniq):
            return{
                'id': uniq.id,
                'name': uniq.name,
                'genres': uniq.genres,
                'city': uniq.city,
                'state':uniq.state,
                'phone': uniq.phone,
                'search_venue': uniq.search_venue,
                'search_description': uniq.search_description,
                'image_link': uniq.image_link,
                'web_site': uniq.web_site,
                'facebook_link': uniq.facebook_link,

            }



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.












#show model
class Show(db.Model):

    __tablename__ = 'Show'
    id = db.Column(Integer,primary_key=True)
    venue_id = db.Column(Integer, ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(Integer, ForeignKey(Artist.id), nullable=False)
    starting_time = db.Column(String(), nullable=False)


    def __init__(uniq, venue_id,artist_id,starting_time):
        uniq.venue_id = venue_id
        uniq.artist_id = artist_id
        uniq.starting_time = starting_time

    def insert(uniq):
        db.session.add(uniq)
        db.session.commit()

    def detail(uniq):
        return{
            'venue_id' :uniq.venue_id,
            'venue_name' :uniq.Venue.name,
            'artist_id' :uniq.artist_id,
            'artist_name' :uniq.Artist.name,
            'artist_image_link' :uniq.Artist.image_link,
            'starting_time' :uniq.starting_time
        }

    def artist_details(uniq):
        return{
            'artist_id' :uniq.venue_id,
            'artist_name' :uniq.Artist.name,
            'artist_image_link' :uniq.Artist.image_link,
            'starting_time' :uniq.starting_time

        }
 
    
    def venue_details(uniq):
        return{
            'venue_id' :uniq.venue_id,
            'venue_name' :uniq.Venue.name,
            'venue_image_link' :uniq.Venue.image_link,
            'starting_time' :uniq.starting_time
            
        }
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
   current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
   venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
   venue_state_and_city = ''
   data = []

   for venue in venues:
    print(venue)
    upcoming_shows = venue.shows.filter(Show.start_time > current_time).all()
    if venue_state_and_city == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name":venue.name,
        "num_upcoming_shows": len(upcoming_shows) 
      })
    else:
      venue_state_and_city == venue.city + venue.state
      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })
   return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"


  query_venue = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  get_venue_list = list(map(Venue.short, query_venue))
  
  response={
    "count": len(get_venue_list),
    "data": get_venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue_query = Venue.query.get(venue_id)
  if venue_query:
    venue_details = Venue.detail(venue_query)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time > current_time).all()
    new_show = list(map(Show.artist_details, new_shows_query))
    venue_details["upcoming_shows"] = new_show
    venue_details["upcoming_shows_count"] = len(new_show)
    past_shows_query = Show.query.options(db.joinedload(Show.Venue)).filter(Show.venue_id == venue_id).filter(Show.start_time <= current_time).all()
    past_shows = list(map(Show.artist_details, past_shows_query))
    venue_details["past_shows"] = past_shows
    venue_details["past_shows_count"] = len(past_shows)
    return render_template('pages/show_venue.html', venue=venue_details)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   try:
          new_venue = Venue(
          name=request.form['name'],
          genres=request.form.getlist('genres'),
          address=request.form['address'],
          city=request.form['city'],
          state=request.form['state'],
          phone=request.form['phone'],
          web_site=request.form['web_site'],
          facebook_link=request.form['facebook_link'],
          image_link=request.form['image_link'],
          search_talent=request.form['search_talent'],
          description=request.form['search_description'],
        )
    
          Venue.insert(new_venue)
          # on successful db insert, flash success
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
          # TODO: on unsuccessful db insert, flash an error instead.
          # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
          # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

   except SQLAlchemyError as e:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
   return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback() 
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artist_query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
  get_artist_list = list(map(Artist.short, artist_query)) 
  response = {
    "count":len(get_artist_list),
    "data": get_artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  artist_query = Artist.query.get(artist_id)
  if artist_query:
    artist_details = Artist.details(artist_query)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time > current_time).all()
    new_shows_list = list(map(Show.venue_details, new_shows_query))
    artist_details["upcoming_shows"] = new_shows_list
    artist_details["upcoming_shows_count"] = len(new_shows_list)
    past_shows_query = Show.query.options(db.joinedload(Show.Artist)).filter(Show.artist_id == artist_id).filter(Show.start_time <= current_time).all()
    past_shows_list = list(map(Show.venue_details, past_shows_query))
    artist_details["past_shows"] = past_shows_list
    artist_details["past_shows_count"] = len(past_shows_list)
    return render_template('pages/show_artist.html', artist=artist_details)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data = Artist.query.get(artist_id)
  if artist_data:
    artist_details = Artist.details(artist_data)
    form.name.data = artist_details["name"]
    form.genres.data = artist_details["genres"]
    form.city.data = artist_details["city"]
    form.state.data = artist_details["state"]
    form.phone.data = artist_details["phone"]
    form.web_site.data = artist_details["web_site"]
    form.facebook_link.data = artist_details["facebook_link"]
    form.search_venue.data = artist_details["search_venue"]
    form.search_description.data = artist_details["search_description"]
    form.image_link.data = artist_details["image_link"]
    return render_template('forms/edit_artist.html', form=form, artist=artist_details)
  # TODO: populate form with fields from artist with ID <artist_id>


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
 form = ArtistForm(request.form)
 artist_data = Artist.query.get(artist_id)
 if artist_data:
        if form.validate():
            search_venue = False
            search_description = ''
            if 'search_venue' in request.form:
                search_venue = request.form['search_venue'] == 'y'
            if 'search_description' in request.form:
                search_description = request.form['search_description']
            setattr(artist_data, 'name', request.form['name'])
            setattr(artist_data, 'genres', request.form.getlist('genres'))
            setattr(artist_data, 'city', request.form['city'])
            setattr(artist_data, 'state', request.form['state'])
            setattr(artist_data, 'phone', request.form['phone'])
            setattr(artist_data, 'web_site', request.form['web_site'])
            setattr(artist_data, 'facebook_link', request.form['facebook_link'])
            setattr(artist_data, 'image_link', request.form['image_link'])
            setattr(artist_data, 'search_description', search_description)
            setattr(artist_data, 'search_venue', search_venue)
            Artist.update(artist_data)
 return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_query = Venue.query.get(venue_id)
  if venue_query:
    venue_details = Venue.detail(venue_query)
    form.name.data = venue_details["name"]
    form.genres.data = venue_details["genres"]
    form.address.data = venue_details["address"]
    form.city.data = venue_details["city"]
    form.state.data = venue_details["state"]
    form.phone.data = venue_details["phone"]
    form.web_site.data = venue_details["web_site"]
    form.facebook_link.data = venue_details["facebook_link"]
    form.search_talent.data = venue_details["search_talent"]
    form.search_description.data = venue_details["search_description"]
    form.image_link.data = venue_details["image_link"]
    return render_template('form/edit_venue.html', form=form, Venue=venue_details)
  # TODO: populate form with values from venue with ID <venue_id>

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  form = VenueForm(request.form)
  venue_data = Venue.query.get(venue_id)
  if venue_data:
      if form.validate():
          search_talent = False
          search_description = ''
          if 'search_talent' in request.form:
              search_talent = request.form['search_talent'] == 'y'
          if 'search_description' in request.form:
              search_description = request.form['search_description']
          setattr(venue_data, 'name', request.form['name'])
          setattr(venue_data, 'genres', request.form.getlist('genres'))
          setattr(venue_data, 'address', request.form['address'])
          setattr(venue_data, 'city', request.form['city'])
          setattr(venue_data, 'state', request.form['state'])
          setattr(venue_data, 'phone', request.form['phone'])
          setattr(venue_data, 'website', request.form['website'])
          setattr(venue_data, 'facebook_link', request.form['facebook_link'])
          setattr(venue_data, 'image_link', request.form['image_link'])
          setattr(venue_data, 'search_description', search_description)
          setattr(venue_data, 'search_talent', search_talent)
          Venue.update(venue_data)
      return redirect(url_for('show_venue', venue_id=venue_id))
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
    search_venue = False
    search_description = ''
    if 'search_venue' in request.form:
      search_venue = request.form['search_venue'] == 'y'
    if 'search_description' in request.form:
      search_description = request.form['search_description']
    new_artist = Artist(
      name=request.form['name'],
      genres=request.form['genres'],
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      website=request.form['web_site'],
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      search_venue=search_venue,
      search_description=search_description,
    )
    Artist.insert(new_artist)
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except SQLAlchemyError as e:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + request.form['name'] + 'could not be listed. ')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  show_query = Show.query.options(db.joinedload(Show.Venue), db.joinedload(Show.Artist)).all()
  data = list(map(Show.detail, show_query))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    new_show = Show(
      venue_id=request.form['venue_id'],
      artist_id=request.form['artist_id'],
      start_time=request.form['start_time'],
    )
    Show.insert(new_show)

    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except SQLAlchemyError as e:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occured. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
