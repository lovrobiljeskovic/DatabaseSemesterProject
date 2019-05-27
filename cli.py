import sys
import mysql.connector

sys.path.append('./map')

import map

def find_book_titles_city_name(city_name):
    result = sqlQuery("""SELECT * FROM book_titles INNER JOIN authors ON book_titles.book_id = authors.book_id
    INNER JOIN book_cities ON book_cities.book_id = book_titles.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id 
    WHERE cities.asciiname = """ + "'" + city_name + "'")
    for row in result:
        print(row)

def plot_cities_by_book_titles(book_titles):
    result = sqlQuery(" SELECT latitude, longitude, asciiname FROM book_titles INNER JOIN book_cities ON book_titles.book_id = book_cities.book_id INNER JOIN cities ON cities.geonameid = book_cities.city_id WHERE book_titles.title = '" + book_titles + "'")
    m = map.Map(result)
    m.open()
def rootconnect():
    pw = '1234'
    conn = mysql.connector.connect( host='localhost', database='noob',user='root', password=pw, auth_plugin='mysql_native_password')
    conn.autocommit = True
    print("CONNECTION --" + str(conn))
    return conn

conn = rootconnect()
    
def sqlQuery(sqlString):
    global conn
    try:
        if not conn.is_connected():
            conn = rootconnect()
        cursor = conn.cursor()
        cursor.execute(sqlString)
        res = cursor.fetchall()
        return res
    except Exception as ex:
        print(str(ex), file=sys.stderr)
    finally:    
        cursor.close()

def sqlDo(sqlString):
    global conn
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

while True:
    print("1. Find book titles by city name")
    print("2. See a map of the cities mentioned in the book titles")
    print("3. List all books by a specific author")
    print("4. List all books by a specific location")
    print("5. exit")
    options = input("Choose one of the options above")
    print(options)
    if options == "1":
        city_name = input("enter city name pls")
        find_book_titles_city_name(city_name)
    elif options == 2:
        book_titles = input("enter book title pls")
        plot_cities_by_book_titles(book_titles)
    elif options == 3:
        author = input("enter the name of the author pls")


if __name__ == "__main__":
    find_book_titles_city_name(city_name)






