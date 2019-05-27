import string
import webbrowser
import random
import os

class Map:
    
    filePath = '';

    def __init__(self, data, flip = False):
        dataString = self.formatData(data, flip)
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

    def formatData(self, data, flip = False):
        s=""
        for lat,lon,*other in data:
            comments = "\n".join([str(i) for i in other])
            comments = comments.replace("\r", "")
            comments = comments.replace("\n", "<br/>")
            comments = comments.replace("\"", "\\\"")
                
            coords = str(lat) + ", " + str(lon)
            if flip:
                coords = str(lon) + ", " + str(lat)
            s += "{c: [" + coords + "], t: \"" + comments + "\"},\n"
        return s

    def __del__(self):
        self.close()
                