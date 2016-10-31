from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.core.window import Window

import requests # Brukes til å sende og hente. (kivy -m pip install requests )
import bs4 # Håndtering av XML (kivy -m pip install bs4)
import xml.etree.ElementTree as ET # Alternativt bibliotek for XML-parsing (kivy -m pip install lxml)
import datetime # Brukes for å få differensen mellom to tider enklere

SOAP_ACTION_GET_STOP_MONITORING = "GetStopMonitoring"
NODE_MONITORED_VEHICLE_JOURNEY = "MonitoredVehicleJourney"

SIRI_SM_SERVICE = "http://st.atb.no/SMWS/SMService.svc"
SIRI_NAMESPACE = "http://www.siri.org.uk/siri"

# Bus-stop identifier. Available at AtB's webpages.
STOP_ID = "16011192" # Ila mot sentrum



import datetime

class Buss:
    def __init__(self, node):
        self.node = node

    def addAimedTime(self,aimedTime):
        self.aimedTime = aimedTime

    def addExpectedTime(self, expectedTime):
        self.expectedTime = expectedTime

    def returnAimedTime(self):
        return self.aimedTime

    def returnExpectedTime(self):
        return self.expectedTime

    def getExpectedUntilDeparture(self):
        if self.expectedTime == None:
            return None

        now = datetime.datetime.now()
        expected = datetime.datetime.combine(now, self.expectedTime)
        return expected - now

    def getAimedUntilDeparture(self):
        if self.aimedTime == None:
            return None

        now = datetime.datetime.now()
        aimed = datetime.datetime.combine(now, self.aimedTime)
        return aimed - now


    def addLine(self, line):
        self.line = line

    def returnNode(self):
        return self.node

    def getLine(self):
        return self.line

    def setDisplay(self,disp):
        self.disp = disp

    def getDisplay(self):
        return self.disp

    def setStop(self,stopName):
        self.stopName = stopName

    def getStop(self):
        return self.stopName




def getBusObj(tree):
    """ Given a tree corresponding to the desired bus-stop, and line-no, this
    function will return a list of tuples (index, time_struct) corresponding to
    the buses in the given tree "tree". """


    root = tree.getroot()

    myBuses = []


    # Navigate the tree (consider collecting loops)
    curChild = None
    for child in root:
        if child.tag[-4:] == "Body":
            curChild = child

    for child in curChild:
        if child.tag == "GetStopMonitoringResponse":
            curChild = child

    for child in curChild:
        if child.tag == "Answer":
            curChild = child

    for child in curChild:
        if child.tag == "StopMonitoringDelivery":
            curChild = child

    # Extract the "buses"
    for child in curChild:
        if child.tag == "MonitoredStopVisit":
            for subChild in child:
                if subChild.tag == "MonitoredVehicleJourney":
                    myBuses.append(Buss(subChild))

    # Find Line, StopName, Display text
    for bus in myBuses:
        for node in bus.node:
            if node.tag == "LineRef":
                bus.addLine(node.text.strip())
            if node.tag == "MonitoredCall":
                for snode in node:
                    if snode.tag == "StopPointName":
                        bus.setStop(snode.text.strip())
                    if snode.tag == "DestinationDisplay":
                        bus.setDisplay(snode.text.strip())

    # Extract times (WARN: skjeten kode ahead!)
    i = 0
    j = 0
    for bus in myBuses:
        for node in bus.node:
            if node.tag == "MonitoredCall":
                for subnode in node:
                    if subnode.tag == "AimedDepartureTime":
                        aimedTime = subnode.text
                        aimedTime = aimedTime.replace("\n", "")
                        aimedTime = aimedTime.replace(" ", "")
                        aimedTime = aimedTime[11:19]
                        dt_obj = datetime.datetime.strptime(aimedTime, "%H:%M:%S")
                        aimedTimeHour = dt_obj.hour
                        aimedTimeMin = dt_obj.minute
                        aimedTimeSec = dt_obj.second
                        aimedTime = datetime.time(aimedTimeHour,
                                                  aimedTimeMin,
                                                  aimedTimeSec)
                        bus.addAimedTime(aimedTime)
                        i = i + 1
                    if subnode.tag == "ExpectedDepartureTime":
                        expectedTime = subnode.text
                        expectedTime = expectedTime.replace("\n", "")
                        expectedTime = expectedTime.replace(" ", "")
                        expectedTime = expectedTime[11:19]
                        dt_obj = datetime.datetime.strptime(expectedTime, "%H:%M:%S")
                        expectedTimeHour = dt_obj.hour
                        expectedTimeMin = dt_obj.minute
                        expectedTimeSec = dt_obj.second
                        expectedTime = datetime.time(expectedTimeHour,
                                                     expectedTimeMin,
                                                     expectedTimeSec)
                        bus.addExpectedTime(expectedTime)
                        j = j + 1

    return myBuses

def getEnvelope(stopId, namespace):
    return ("<S:Envelope xmlns:S='http://schemas.xmlsoap.org/soap/envelope/' xmlns:s='http://www.siri.org.uk/siri' xmlns:b='" + namespace + "'>" +
            "   <S:Body>" +
            "       <b:GetStopMonitoring>" +
            "           <ServiceRequestInfo>" +
            "               <s:RequestorRef>NAME OF BACKEND</s:RequestorRef>" +
            "           </ServiceRequestInfo>" +
            "           <Request version='1.4'>" +
            "               <s:PreviewInterval>P0DT5H0M0.000S</s:PreviewInterval>" +
            "               <s:MonitoringRef>" + stopId + "</s:MonitoringRef>" +
            "           </Request>" +
            "       </b:GetStopMonitoring>" +
            "   </S:Body>" +
            "</S:Envelope>")


def getXML(stopId, namespace, url):

    body = getEnvelope(STOP_ID, SIRI_NAMESPACE)
    headers = {'Content-type': 'text/xml; charset=UTF-8', "SOAPAction": SOAP_ACTION_GET_STOP_MONITORING}

    response = requests.post(SIRI_SM_SERVICE, data=body, headers=headers)

    if response.status_code != 200:
        print("Error code: ", end='')
        print(response.status_code)
        return

    soup = bs4.BeautifulSoup(response.content, "lxml-xml", from_encoding='UTF-8')

    f = open("AtB.xml", "wb")
    f.write(soup.prettify(encoding='UTF-8',formatter='minimal')) # Lagrer en xml fil som er 'pretty'.
    f.close()


kv = '''
<MyClockWidget>:
    ticks: ticks

    Ticks:
        id: ticks
'''
Builder.load_string(kv)

class MyClockWidget(FloatLayout):
    pass

class Ticks(Widget):
    def __init__(self, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)

    def update_clock(self, *args):

        myB = []
        i = 0
        while (len(myB) < 4):
            if (MyClockApp().busObjs[i].getLine() == "11" or MyClockApp().busObjs[i].getLine() == "5" or MyClockApp().busObjs[
                i].getLine() == "8" or MyClockApp().busObjs[i].getLine() == "63" or MyClockApp().busObjs[i].getLine() == "18"):
                myB.append(MyClockApp().busObjs[i])
            i = i + 1


        self.canvas.clear()
        with self.canvas:
            print("")
            print(myB[0].getStop())
            print("")
            Label(text=myB[0].getStop(), font_size=45, center=(Window.width*0.1, Window.height*0.92))
            """Color(0.2, 0.5, 0.2)
            Line(points=[self.center_x, self.center_y, self.center_x+0.8*self.r*sin(pi/30*time.second), self.center_y+0.8*self.r*cos(pi/30*time.second)], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[self.center_x, self.center_y, self.center_x+0.7*self.r*sin(pi/30*time.minute), self.center_y+0.7*self.r*cos(pi/30*time.minute)], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            th = time.hour*60 + time.minute
            Line(points=[self.center_x, self.center_y, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y+0.5*self.r*cos(pi/360*th)], width=3, cap="round")"""
            #Label(text=str("%d" % (myB[1].getAimedUntilDeparture().seconds / 60)) + " min", font_size=30, center=(Window.width*0.9, Window.height*0.5))


            print("")
            print(myB[0].getDisplay())
            print("")


            lol = myB[0].getDisplay()



            Label(text=lol, font_size=30, center=(Window.width * 0.4, Window.height*0.92))
            Label(text=myB[0].getLine(), font_size=30, center=(Window.width * 0.1, Window.height * (0.75 - 0.5*0)))

            Label(text=str("%d" % (myB[0].getAimedUntilDeparture().seconds / 60)) + " min", font_size=30,
                  center=(Window.width * 0.6, Window.height * (0.75 - 0.5*0)))


            """for j in range(len(myB)):
                Label(text=myB[j].getDisplay(), font_size=30, center=(Window.width*0.4, Window.height*(0.75 - 0.5*j)))
                Label(text=myB[j].getLine(), font_size=30, center=(Window.width*0.1, Window.height*(0.75 - 0.5*j)))

                try:
                    Label(text=str("%d" % (myB[j].getExpectedUntilDeparture().seconds / 60)) + " min", font_size=30,
                              color=[1, 1, 0.5, 0.9], center=(Window.width*0.6, Window.height*(0.75 - 0.5*j)))
                except:
                    Label(text=str("%d" % (myB[j].getAimedUntilDeparture().seconds / 60)) + " min", font_size=30,
                          center=(Window.width * 0.6, Window.height * (0.75 - 0.5*j)))"""

def mainRun():
    # Uncomment line below to request new XML-data from AtB
    getXML(STOP_ID, SIRI_NAMESPACE, SIRI_SM_SERVICE)
    tree = ET.parse('AtB.xml')
    busObjs = getBusObj(tree)

    """print(busObjs[0].getStop())
    print("")
    print("Ila - mot sentrum")
    print("")
    print("------------------------------------------")
    for i in range(0,6):
        try:
            print('%3s' % busObjs[i].getLine(), '%19s' % busObjs[i].getDisplay(), " Tid: ", busObjs[i].returnExpectedTime().hour, ':', busObjs[i].returnExpectedTime().minute)
        except:
            print('%3s' % busObjs[i].getLine(), '%19s' % busObjs[i].getDisplay(), " Tid: ", busObjs[i].returnAimedTime().hour, ':', busObjs[i].returnAimedTime().minute)
        print("------------------------------------------")
    print("")"""

    return busObjs


class MyClockApp(App):
    busObjs = mainRun()

    def build(self):
        clock = MyClockWidget()
        Clock.schedule_interval(clock.ticks.update_clock, 30)
        return clock

if __name__ == '__main__':
    MyClockApp().run()