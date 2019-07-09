"""Populate the database with venues stored in venues.json."""

import json
from pathlib import Path
import requests


base_path = Path(__file__).parent
venue_data = (base_path / 'static' / 'venues.json').read_text()
review_data = (base_path / 'static' / 'ratings.json').read_text()
venues = json.loads(venue_data)['venues']
ratings = json.loads(review_data)['ratings']


if __name__ == '__main__':
    for venue in venues:
        response = requests.post(
            'http://localhost:5000/add/venue',
            json=venue,
        )
        print(response.json())
    for rating in ratings:
        response = requests.post(
            'http://localhost:5000/add/rating',
            json=rating,
        )
        print(response.json())
