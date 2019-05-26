import string
import webbrowser
import random
import os

class Map:
    
    filePath = '';

    def __init__(self, data):
        dataString = self.formatData(data)
        d =  os.path.abspath(os.path.dirname(__file__))
        templatePath = d + "/template.html"
        self.filePath = d + "/" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        with open(templatePath, 'r') as templateFile, open(self.filePath, "w") as mapFile:
            content = templateFile.read().replace("{data}", dataString)
            mapFile.write(content)
    
    def open(self):
        webbrowser.open(self.filePath, new=2)
    
    def close(self):
        os.remove(self.filePath)

    def formatData(self, data):
        s=""
        for lat,lon,*other in data:
            comments = str("".join(other)).replace("\"", "\\\"")

            s += "{c: [" + str(lat) + ", " + str(lon) + "], t: \"" + comments + "\"},"
        return s

    def __del__(self):
        self.close()
                

map = Map([
    [55.676111, 12.568333, """It's a Copenhagen"""],
]);
map.open();
input("Press enter to coninue")