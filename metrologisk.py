from PIL import Image
from io import StringIO, BytesIO
from urllib.request import urlretrieve



class getDataFormMet(object):

    

    def getRadarImage:
        
        imgUrl="http://api.met.no/weatherapi/radar/1.5/?radarsite=central_norway;type=reflectivity;content=animation;size=normal"
        imgUrl2='http://weknowyourdreams.com/images/egg/egg-01.jpg'
        

        imgStr='radarimg' + '.gif'
        urlretrieve(imgUrl, imgStr)
        radarImg = Image.open(imgStr)
        radarImg.show()





    #http://api.met.no/weatherapi/radar/1.5/documentation

    
    pass






