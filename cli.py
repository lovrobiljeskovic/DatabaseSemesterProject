import sys
import mysql.connector
import pymongo
import time
from pymongo import MongoClient

sys.path.append('./map')

import map

def get_millis():
    return int(round(time.time() * 1000))


class Mysql:
    conn = None

    def __init__(self):
        self.conn = self.rootconnect()

    def find_book_titles_city_name(self, city_name):
        result = self.sqlQuery("""SELECT book_titles.title FROM book_titles INNER JOIN authors ON book_titles.book_id = authors.book_id
        INNER JOIN book_cities ON book_cities.book_id = book_titles.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id 
        WHERE cities.asciiname = """ + "'" + city_name + "'")
        for row in result:
            print(row)
        print("\n\n")

    def plot_cities_by_book_titles(self, book_titles):
        result = self.sqlQuery(" SELECT latitude, longitude, asciiname FROM book_titles INNER JOIN book_cities ON book_titles.book_id = book_cities.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id WHERE book_titles.title = '" + book_titles + "'")
        m = map.Map(result)
        m.open()
        input("press enter to coninute")

    def plot_cities_by_book_author(self, author):
        result = self.sqlQuery("""
                SELECT latitude, longitude, CONCAT('"', book_titles.title, '"', ' ', authors.name, book_titles.book_id, '"', cities.asciiname, '"') FROM authors 
                INNER JOIN book_titles ON authors.book_id = book_titles.book_id 
                INNER JOIN book_cities ON book_cities.book_id = authors.book_id
                INNER JOIN cities ON cities.geonameid = book_cities.city_id WHERE authors.name = '""" + author + "' OR authors.first_name = '" + author + "'")
        m = map.Map(result)
        m.open()
        input("press enter to coninute")

    def list_books_by_city_location(self, latitude, longitude, distance = 10000):
        f = latitude + " " + longitude
        result = self.sqlQuery("""
            SELECT distinct(cities.asciiname), title, ST_Distance(cities.location, ST_GeomFromText('POINT(""" + f + """)', 4326)) as distance 
            FROM cities 
            INNER JOIN book_cities ON cities.geonameid = book_cities.city_id 
            INNER JOIN book_titles ON book_titles.book_id = book_cities.book_id 
            HAVING distance > 1 AND distance <= """ + str(distance))

        for row in result:
            print(row)
        print("\n\n")
        

    def rootconnect(self):
        pw = 'secret'
        conn = mysql.connector.connect( host='localhost', database='db_exam',user='root', password=pw, auth_plugin='mysql_native_password')
        conn.autocommit = True
        return conn
            
    def sqlQuery(self, sqlString):
        conn = self.conn
        try:
            if not conn.is_connected():
                conn = rootconnect()
            cursor = conn.cursor()
            millis = get_millis()
            cursor.execute(sqlString)
            print(str(get_millis() - millis) + " MS")
            res = cursor.fetchall()
            return res
        except Exception as ex:
            print(str(ex), file=sys.stderr)
        finally:    
            cursor.close()

    def sqlDo(self, sqlString):
        conn = self.conn
        try:
            if not conn.is_connected():
                conn = rootconnect()
            cursor = conn.cursor()
            cursor.execute(sqlString)
            res = cursor.fetchwarnings()
            return res
        except Exception as ex:
            print(str(ex), file=sys.stderr)
        finally:    
            cursor.close()


class Mongo:
    client = None
    conn = None

    def __init__(self):
        self.client = MongoClient()
        self.conn = self.client.db_exam.books

    def find_book_titles_city_name(self, city_name):
        result = self.conn.find({ "cities": {"$elemMatch": {"name": city_name } } })
        for row in result:
            print(row["title"])
        print("\n\n")

    def plot_cities_by_book_titles(self, book_titles):
        result = self.conn.find({'title': book_titles})
        
        betterResult = []
        for row in result: 
            for city in row["cities"]:
                if city["name"] is None: 
                    continue
                betterResult.append((city["location"]["coordinates"][0], city["location"]["coordinates"][1], str(city["name"])))
        m = map.Map(betterResult)
        m.open()
        input("press enter to coninute")

    def plot_cities_by_book_author(self, author):
        result = self.conn.find({'authors': author})

        betterResult = []
        for row in result: 
            for city in row["cities"]:
                if city["name"] is None: 
                    continue
                betterResult.append((city["location"]["coordinates"][0], city["location"]["coordinates"][1], str(city["name"])))
        m = map.Map(betterResult)
        m.open()
        input("press enter to coninute")

    def list_books_by_city_location(self, latitude, longitude, distance = 10000):
        result = self.conn.find(
            {"cities.location": { 
                '$near': { 
                    '$geometry': { 
                        'type': 'Point', 'coordinates': [float(longitude), float(latitude)]
                    },
                    '$maxDistance': distance, 
                    '$minDistance': 1 
                } 
            }  
        });


        for row in result:
            print(row["title"])
        print("\n\n")
        



db = Mysql()

#db.list_books_by_city_location("55.67594", "12.56553")

while True:
    print("1. Find book titles by city name")
    print("2. See a map of the cities mentioned in the book titles")
    print("3. List all books by a specific author")
    print("4. List all books by a specific location")
    print("5. exit")
    options = input("Choose one of the options above: ")
    print(options)
    if options == "1":
        city_name = input("enter city name pls: ")
        db.find_book_titles_city_name(city_name)
    elif options == "2":
        book_titles = input("enter book title pls: ")
        db.plot_cities_by_book_titles(book_titles)
    elif options == "3":
        author = input("enter the name of the author pls: ")
        db.plot_cities_by_book_author(author)
    elif options == "4":
        latitude = input("enter latitude: ")
        longitude = input("enter longitude: ")
        db.list_books_by_city_location(latitude, longitude)

    elif options == "5":
        break
    else:
        print("unknown option \"" + options + "\"\n")