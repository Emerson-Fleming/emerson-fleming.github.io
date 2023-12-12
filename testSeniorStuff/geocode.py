import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Initialize the geocoder
geolocator = Nominatim(user_agent="university_geocoder")

# Function to get country from coordinates


def get_country(latitude, longitude):
    try:
        location = geolocator.reverse((latitude, longitude), language='en')
        if location and 'country' in location.raw['address']:
            return location.raw['address']['country']
    except (GeocoderTimedOut, GeocoderUnavailable):
        return "Error in geocoding"

# Function to add country to each university in a JSON file


def add_country_to_universities(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        universities = json.load(file)

    # Update each university with its country
    for university in universities:
        country = get_country(university['latitude'], university['longitude'])
        university['country'] = country if country else "Country not found"

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(universities, file, indent=4)


# File path to your JSON file
file_path = 'universities_worldwide_async.json'

# Add country to each university in the file
add_country_to_universities(file_path)