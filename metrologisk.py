from io import StringIO, BytesIO
from urllib.request import urlretrieve

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout


class metApp(App):
    def build(self):

        rootL=FloatLayout()
        s=Scatter()
        l=Label(text="Det blir sol og fint!!",font_size=150)

        metData=getDataFormMet(icontent='animation')
        imgUrl=metData.getRadarImage()

        p=AsyncImage(source=imgUrl)

        rootL.add_widget(s)
        s.add_widget(p)

        return rootL

class getDataFormMet(object):

    def __init__(self,iradarsite='central_norway',itype='reflectivity',icontent='aniation',isize='normal'):
        self.radarsite=iradarsite
        self.type=itype
        self.content=icontent
        self.size=isize

    def getRadarImage(self):
        #Buliding the URL for the request
        
        imgUrl='http://api.met.no/weatherapi/radar/1.5/?radarsite='+self.radarsite+';type='+self.type+';content='+self.content+';size='+self.size
        #imgUrl='http://api.met.no/weatherapi/radar/1.5/?radarsite=central_norway;type=reflectivity;content=animation;size=normal'

        #print(imgUrl)
        return imgUrl
        #return imgUrl


    #http://api.met.no/weatherapi/radar/1.5/documentation

    
    pass


#print(metData.getRadarImage())

if __name__ == '__main__':
    metApp().run()