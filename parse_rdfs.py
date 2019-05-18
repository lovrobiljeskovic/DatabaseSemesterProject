import os
from os.path import isfile, join
import rdflib
from rdflib.namespace import DCTERMS,Namespace

def pgen(gen):
    for a, b, c in gen:
        print("a=" + str(a) + "b=" + str(b) + "c=" + str(c))

def get_authors(g):
    authors = []
    for child in g.objects(None, DCTERMS["creator"]):
        #pgen(g.triples((child, PGTERMS["name"], None)))
        for a in g.objects(child, PGTERMS["name"]):
            authors.append(a)
    return authors


def get_title(g):
    for title in g.objects(None, DCTERMS["title"]):
        return title

def write_authors(file, authors):
    for author in authors:
        names = author.split(",")
        line = bookId + ",\"" + author + "\"";
        if len(names) >= 2:
            line += "," + names[0].strip() + "," + names[1].strip()
        else:
            line += ",,"
        file.write(line + "\n")

def write_title(file, title):
    title = title.encode('unicode_escape').decode("utf-8")
    title = title.replace("\"", "\\\"")
    titleFile.write(bookId + ",\"" + title + "\"\n")

PGTERMS=Namespace('http://www.gutenberg.org/2009/pgterms/')

#bookNumbers=["9910", "30054", "26652"]

# Change this to point to the directory for RDF folders
bookFolder="../rdf/"

#(root,dirs,*files) = os.walk(bookFolder)
bookPaths = [f for f in os.listdir(bookFolder) if not isfile(f)]


with open("authors.csv", 'w') as authorFile, open("titles.csv", 'w') as titleFile:
    authorFile.write("bookId,name,first_name,last_name\n")
    titleFile.write("bookId,title\n")

    for bookPath in bookPaths:
        parts = bookPath.split("/")
        bookId = parts[-1]
        print("bookId="+ bookId)
        g=rdflib.Graph()
        g.bind('dcterms', DCTERMS)
        g.bind('pgterms', PGTERMS)
        try:
            g.load(bookFolder + bookId + '/pg' + bookId + '.rdf')
        except Exception as e:
            print("cannot load boook " + bookId + ":" + str(e))
            continue

        authors = get_authors(g)
        if len(authors) > 0:
            write_authors(authorFile, authors)
            
        title = get_title(g)
        #print("authors=" + "/".join(get_authors(g)) + " title=" + str(title))
        if title is not None:
            write_title(titleFile, title)

