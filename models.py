from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    serialize_rules = ('-appearances.episode',)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # Relationship
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Episode {self.id}: {self.date}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-appearances.guest',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # Relationship
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Guest {self.id}: {self.name}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # Validation
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is None:
            raise ValueError("Rating is required")
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def __repr__(self):
        return f'<Appearance {self.id}: Episode {self.episode_id}, Guest {self.guest_id}, Rating {self.rating}>'
