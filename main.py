from geotext import GeoText
import pandas as pd
import os
from os.path import isfile, join

def find_locations(text,ner_tagger):

    # Prepare NER tagger with english model
    #ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

    # Tokenize: Split sentence into words
    words = nltk.word_tokenize(text)

    # Run NER tagger on words
    return ner_tagger.tag(words)

def find_location_geo(text):
# print(places.cities)
    return GeoText(text).cities   


def filter_locations(book_locations,df):       
    
    return [df[df.asciiname == i].iloc[0].geonameid for i in book_locations if i in list(df.asciiname)]


labels = ["geonameid", "name", "asciiname", "alternatenames",'latitude',
          'longitude','feature class','feature code','country code','cc2','admin1 code','admin2 code',
         'admin3 code','admin4 code','population','elevation','dem','timezone','modification date']

df = pd.read_csv('./../cities5000.txt', sep='\t',names = (labels))

df = df[['geonameid','asciiname','latitude','longitude']]

# Change this to point to the directory for RDF folders
bookFolder="../files/"

bookPaths = [bookFolder + f for f in os.listdir(bookFolder) if isfile(bookFolder + f)]


with open("book_cities.csv", "w") as outputFile:
    outputFile.write("bookId,geonameId\n")
    for bookPath in bookPaths:
        print("bookPath:" + str(bookPath))
        try :
            with open(bookPath, 'r') as bookContentFile:
                parts = bookPath.split("/")
                fileName = parts[-1]
                parts = fileName.split(".")
                bookId = parts[0]
                
                print("bookId " + str(bookId))
                bookContent = bookContentFile.read()
                #print(bookContent)
                book_locations = find_location_geo(bookContent)        
                locations = filter_locations(book_locations,df)            
                #print(set(locations))
                for location in set(locations):
                    outputFile.write(bookId + "," + str(location) + "\n")
        except Exception as e:
            print(bookPath + " failed " + str(e))