import nltk
from nltk.tag.stanford import StanfordNERTagger
from geotext import GeoText
import pandas as pd

jar = './stanford-ner.jar'
model = './english.all.3class.distsim.crf.ser.gz'
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

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
    
print(set(filter_locations(book_locations,list(df.asciiname))))