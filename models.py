# all classes are defined here together with the methods
from db import get_connection

class Concert:
    @staticmethod
    def band(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.id = ?
        ''', (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def venue(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT venues.title, venues.city
            FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.id = ?
        ''', (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def hometown_show(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT (venues.city = bands.hometown) AS is_hometown
            FROM concerts
            JOIN bands ON concerts.band_name = bands.name
            JOIN venues ON concerts.venue_title = venues.title
            WHERE concerts.id = ?
        ''', (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] == 1

    @staticmethod
    def introduction(concert_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT "Hello " || venues.city || "!!!!! We are " || bands.name || " and we're from " || bands.hometown
            FROM concerts
            JOIN bands ON concerts.band_name = bands.name
            JOIN venues ON concerts.venue_title = venues.title
            WHERE concerts.id = ?
        ''', (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0]

class Band:
    @staticmethod
    def concerts(band_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE band_name = ?
        ''', (band_name,))
        results = cursor.fetchall()
        conn.close()
        return results

    @staticmethod
    def venues(band_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT venues.title, venues.city
            FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.band_name = ?
        ''', (band_name,))
        results = cursor.fetchall()
        conn.close()
        return results

    @staticmethod
    def play_in_venue(band_name, venue_title, date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO concerts (band_name, venue_title, date)
            VALUES (?, ?, ?)
        ''', (band_name, venue_title, date))
        conn.commit()
        conn.close()

    @staticmethod
    def all_introductions(band_name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT "Hello " || venues.city || "!!!!! We are " || bands.name || " and we're from " || bands.hometown
            FROM concerts
            JOIN bands ON concerts.band_name = bands.name
            JOIN venues ON concerts.venue_title = venues.title
            WHERE bands.name = ?
        ''', (band_name,))
        results = cursor.fetchall()
        conn.close()
        return [result[0] for result in results]

    @staticmethod
    def most_performances():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            GROUP BY bands.name
            ORDER BY COUNT(concerts.id) DESC
            LIMIT 1
        ''')
        result = cursor.fetchone()
        conn.close()
        return result[0]

class Venue:
    @staticmethod
    def concerts(venue_title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE venue_title = ?
        ''', (venue_title,))
        results = cursor.fetchall()
        conn.close()
        return results

    @staticmethod
    def bands(venue_title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT bands.name, bands.hometown
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.venue_title = ?
        ''', (venue_title,))
        results = cursor.fetchall()
        conn.close()
        return results

    @staticmethod
    def concert_on(venue_title, date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE venue_title = ? AND date = ?
            LIMIT 1
        ''', (venue_title, date))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def most_frequent_band(venue_title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name
            FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.venue_title = ?
            GROUP BY bands.name
            ORDER BY COUNT(concerts.id) DESC
            LIMIT 1
        ''', (venue_title,))
        result = cursor.fetchone()
        conn.close()
        return result[0]
