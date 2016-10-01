from PIL import Image
from io import StringIO, BytesIO
import urllib.request



class getDataFormMet(object):

    

    def getRadarImage:
        
        #imgUrl="http://api.met.no/weatherapi/radar/1.5/?radarsite=central_norway;type=reflectivity;content=animation;size=normal"
        imgUrl2='http://weknowyourdreams.com/images/egg/egg-01.jpg'
        imgUrl3='http://python.org/'
        
        
        radarResponse=urllib.request.urlopen(imgUrl2)
        
        #radarImg = Image.open(BytesIO(radarResponse.content))
        
        #radarImg = Image.open(StringIO(radarResponse.read()))

        radarImg = Image.open(BytesIO(radarResponse.read())





    #http://api.met.no/weatherapi/radar/1.5/documentation

    
    pass




