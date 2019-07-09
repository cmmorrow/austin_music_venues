"""This module is the self-contained ORM and REST API backend."""

import datetime
from typing import List

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://demo:demo@localhost:5433/amvdb"
)
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Venue(db.Model):
    """A python representation of the venue table."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    name = db.Column(db.String)
    closed = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String)
    description = db.Column(db.String)
    inserted = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    address = db.relationship(
        "Address",
        backref=db.backref('venues', lazy=False),
        uselist=False,
    )
    ratings = db.relationship(
        "Rating",
        backref=db.backref('rated_venue', lazy=False),
        cascade="all, delete, delete-orphan",
    )

    @classmethod
    def get_venues(cls, limit: int = 25) -> List['Venue']:
        """Generate a list of Venues pulled from the database.

        :param limit: The maximum number of Venue objects to return.
        """
        venues = db.session.query(
            Venue.id,
            Venue.name,
            Venue.image_url,
            Venue.description,
            Address.street,
            Address.city,
            Address.state,
            Address.zip,
            Venue.closed,
            db.func.avg(Rating.score).label('rating'),
        ).join(
            Address,
        ).outerjoin(
            Rating,
        ).order_by(
            Venue.name,
        ).group_by(
            Venue.id,
            Address.id,
        ).limit(
            limit,
        ).all()
        return venues

    def __repr__(self) -> str:
        """Defines the instance representation for a Venue object."""
        return (
            '<Venue('
            f'name={self.name}, '
            f'address={self.address.street}, '
            f'image_url={self.image_url[:15]}..., '
            f'description={self.description[:15]}..., '
            f'closed={self.closed}'
            ')>'
        )


class Address(db.Model):
    """A python representation of the venue street address."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, default='Austin')
    state = db.Column(db.String(2), default='TX')
    zip = db.Column(db.String)
    inserted = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self) -> str:
        """Defines the instance representation for an Address object."""
        return (
            '<Address('
            f'id={self.id}, '
            f'street={self.street}, '
            f'city={self.city}, '
            f'state={self.state}, '
            f'zip={self.zip}, '
            f'inserted={self.inserted}'
            ')>'
        )


class Rating(db.Model):
    """A python representation of the rating table."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    score = db.Column(db.Integer)
    review = db.Column(db.String)
    inserted = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @classmethod
    def get_ratings(cls, venue_id: int) -> List['Rating']:
        """Generate a list of Ratings pulled from the database.

        :param venue_id: The venue_id for the corresponding Ratings.
        """
        ratings = db.session.query(
            Rating,
        ).filter(
            Rating.venue_id == venue_id,
        ).all()
        return ratings

    def __repr__(self) -> str:
        """Defines the instance representation for a Rating object."""
        return (
            '<Rating('
            f'id={self.id}, '
            f'venue_id={self.venue_id}, '
            f'score={self.score}, '
            f'review={self.review}, '
            f'inserted={self.inserted}'
            ')>'
        )


@app.route('/', methods=['GET'])
def main():
    """Render the main page."""
    host = request.host_url
    return render_template('main.html', venues=Venue.get_venues(), host=host)


@app.route('/ratings/<venue_id>', methods=['GET'])
def venue_ratings(venue_id: str):
    """Render the ratings page."""
    ratings = Rating.get_ratings(int(venue_id))
    try:
        venue = ratings[0].rated_venue.name
    except IndexError:
        venue = db.session.query(Venue).get(venue_id).name
    return render_template('reviews.html', ratings=ratings, venue=venue)


@app.route('/add/venue', methods=['POST'])
def add_venue():
    """Add a new Venue to the database."""
    payload: dict = request.json
    _venue = payload.get('Venue')
    _address = _venue.get('Address')

    address = db.session.query(
        Address
    ).filter(
        Address.street == _address.get('street'),
        Address.zip == _address.get('zip'),
    ).first()

    if not address:
        address = Address(**_address)
    venue = Venue(
        name=_venue.get('name'),
        closed=_venue.get('closed', False),
        image_url=_venue.get('image_url'),
        description=_venue.get('description'),
        address=address,
    )
    db.session.add(venue)
    db.session.commit()
    return jsonify({'add': 'success'})


@app.route('/add/rating', methods=['POST'])
def add_rating():
    """Add a new Rating to the database."""
    payload: dict = request.json
    _rating = payload.get('Rating')
    venue_id = _rating.get('venue_id')
    score = _rating.get('score')
    review = _rating.get('review')

    rating = Rating(venue_id=venue_id, score=score, review=review)
    db.session.add(rating)
    db.session.commit()
    return jsonify({'add': 'success'})


@app.route('/update/closed', methods=['POST'])
def set_closed():
    """Update the status of a Venue to "closed"."""
    payload: dict = request.json
    venue_id: str = payload['venue_id']

    venue: Venue = db.session.query(Venue).get(venue_id)
    venue.closed = True
    db.session.commit()
    return jsonify({'update': 'success'})


@app.route('/delete/venue', methods=['DELETE'])
def delete_venue():
    """Delete the Venue and attached Ratings associated with venue_id."""
    payload: dict = request.json
    venue_id: str = payload['venue_id']

    venue: Venue = db.session.query(Venue).get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'delete': 'success'})


@app.route('/get/venues', methods=['GET'])
def get_venues():
    """Retrieve a list of Venues from the database."""
    venues: List[Venue] = Venue.get_venues()
    output = {'venues': []}
    for venue in venues:
        _venue = {}
        _venue['id'] = venue.id
        _venue['name'] = venue.name
        _venue['street'] = venue.street
        _venue['city'] = venue.city
        _venue['state'] = venue.state
        _venue['zip'] = venue.zip
        _venue['closed'] = venue.closed
        _venue['image_url'] = venue.image_url
        _venue['description'] = venue.description
        _venue['rating'] = f'{venue.rating:.2f}' if venue.rating else '0.0'
        output['venues'].append(_venue)
    return jsonify(output)


@app.route('/get/ratings/<venue_id>', methods=['GET'])
def get_ratings(venue_id: str):
    """Retrieve a list of Ratings from the database for a certain Venue."""
    ratings: List[Rating] = Rating.get_ratings(int(venue_id))
    output = {'ratings': []}
    for rating in ratings:
        _rating = {}
        _rating['score'] = rating.score
        _rating['review'] = rating.review
        _rating['venue'] = rating.rated_venue.name
        output['ratings'].append(_rating)
    return jsonify(output)
