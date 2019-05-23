from geotext import GeoText
import pandas as pd

def find_location_geo(text):
# print(places.cities)
    return GeoText(text).cities   


def filter_locations(book_locations,locations):

    return [i for i in book_locations if i in locations]


labels = ["geonameid", "name", "asciiname", "alternatenames",'latitude',
          'longitude','feature class','feature code','country code','cc2','admin1 code','admin2 code',
         'admin3 code','admin4 code','population','elevation','dem','timezone','modification date']

df = pd.read_csv('./cities15000.txt', sep='\t',names = (labels))

df = df[['asciiname','latitude','longitude']]

path_2_file = './files_small/10.txt'

book_locations = []
with open(path_2_file) as fp: 
    book_locations = find_location_geo(str(fp.readlines()))

#print(list(df.asciiname))
print(set(filter_locations(book_locations,list(df.asciiname))))