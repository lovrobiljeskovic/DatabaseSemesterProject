from geotext import GeoText

path = './files_small/10.txt'
book_file = open(path,'r')
# print(str(book_file.read()))
places = GeoText("Rio de Janeiro")
print(places.cities)
# print(places.cities)