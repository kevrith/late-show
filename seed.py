#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance
import csv

with app.app_context():
    print("Clearing database...")
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    print("Seeding episodes...")
    episodes_data = [
        {"date": "1/11/99", "number": 1},
        {"date": "1/12/99", "number": 2},
        {"date": "1/13/99", "number": 3},
        {"date": "1/14/99", "number": 4},
        {"date": "1/15/99", "number": 5},
    ]

    episodes = []
    for episode_data in episodes_data:
        episode = Episode(**episode_data)
        episodes.append(episode)
        db.session.add(episode)

    db.session.commit()

    print("Seeding guests...")
    guests_data = [
        {"name": "Michael J. Fox", "occupation": "actor"},
        {"name": "Sandra Bernhard", "occupation": "Comedian"},
        {"name": "Tracey Ullman", "occupation": "television actress"},
        {"name": "Gillian Anderson", "occupation": "actress"},
        {"name": "David Duchovny", "occupation": "actor"},
    ]

    guests = []
    for guest_data in guests_data:
        guest = Guest(**guest_data)
        guests.append(guest)
        db.session.add(guest)

    db.session.commit()

    print("Seeding appearances from CSV...")
    # Try to read from CSV if it exists, otherwise use default data
    try:
        with open('data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                appearance = Appearance(
                    rating=int(row['rating']),
                    episode_id=int(row['episode_id']),
                    guest_id=int(row['guest_id'])
                )
                db.session.add(appearance)
    except FileNotFoundError:
        print("CSV file not found, using default appearances data...")
        appearances_data = [
            {"rating": 4, "episode_id": 1, "guest_id": 1},
            {"rating": 5, "episode_id": 1, "guest_id": 2},
            {"rating": 3, "episode_id": 2, "guest_id": 3},
            {"rating": 5, "episode_id": 2, "guest_id": 4},
            {"rating": 4, "episode_id": 3, "guest_id": 5},
            {"rating": 5, "episode_id": 3, "guest_id": 1},
            {"rating": 3, "episode_id": 4, "guest_id": 2},
            {"rating": 4, "episode_id": 4, "guest_id": 3},
            {"rating": 5, "episode_id": 5, "guest_id": 4},
            {"rating": 4, "episode_id": 5, "guest_id": 5},
        ]

        for appearance_data in appearances_data:
            appearance = Appearance(**appearance_data)
            db.session.add(appearance)

    db.session.commit()

    print("Database seeded successfully!")
