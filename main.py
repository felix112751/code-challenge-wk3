# this is where i perform all my functionalities by using the classes
from db import setup_database
from models import Band, Venue, Concert

# Setup database and tables
setup_database()

# Example usage
band_name = 'The Rockers'
venue_title = 'Rock Arena'
date = '2024-09-15'

# Adding a concert
Band.play_in_venue(band_name, venue_title, date)

# Fetching introductions
introductions = Band.all_introductions(band_name)
print(introductions)

# Checking if a concert is in the band's hometown
concert_id = 1
is_hometown = Concert.hometown_show(concert_id)
print(f"Is hometown show: {is_hometown}")

# Getting the band with the most performances
most_performances_band = Band.most_performances()
print(f"Band with most performances: {most_performances_band}")

# Getting most frequent band at a venue
most_frequent_band = Venue.most_frequent_band(venue_title)
print(f"Most frequent band at {venue_title}: {most_frequent_band}")
