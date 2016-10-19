#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Vennligst ikke fjern linjene over. De blir lest av shell og interpreter.

import kivy # pip install Cython, pip install kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line,Color
from kivy.clock import Clock
from kivy.graphics.instructions import CanvasBase
from kivy.graphics.instructions import VertexInstruction
kivy.require('1.9.1')

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
                        bus.addAimedTime(dt_obj)
                        i = i + 1
                    if subnode.tag == "ExpectedDepartureTime":
                        expectedTime = subnode.text
                        expectedTime = expectedTime.replace("\n", "")
                        expectedTime = expectedTime.replace(" ", "")
                        expectedTime = expectedTime[11:19]
                        dt_obj = datetime.datetime.strptime(expectedTime, "%H:%M:%S")
                        bus.addExpectedTime(dt_obj)
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

def mainRun():
    # Uncomment line below to request new XML-data from AtB
    getXML(STOP_ID, SIRI_NAMESPACE, SIRI_SM_SERVICE)
    tree = ET.parse('AtB.xml')
    busObjs = getBusObj(tree)

    print(busObjs[0].getStop())
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
    print("")

    return busObjs

class MyApp(App):

    busObjs = mainRun()

    def build(self):
        r = FloatLayout()
        l = []
        myB = []

        l.append(Label(text=MyApp().busObjs[0].getStop(), font_size=40, pos_hint={'x': -0.42, 'center_y': 0.91}))

        i = 0
        while (len(myB) < 4):
            if (MyApp().busObjs[i].getLine() == "11" or MyApp().busObjs[i].getLine() == "5" or MyApp().busObjs[i].getLine() == "8" or MyApp().busObjs[i].getLine() == "63" or MyApp().busObjs[i].getLine() == "18"):
                myB.append(MyApp().busObjs[i])
            i = i + 1

        for j in range(len(myB)):
            l.append(Label(text=myB[j].getDisplay(), font_size=30, pos_hint={'x': -0.15, 'center_y': 0.7 - j * 0.05}))
            l.append(Label(text=myB[j].getLine(), font_size=30, pos_hint={'x': -0.4, 'center_y': 0.7 - j * 0.05}))
            try:
                l.append(Label(text=str(myB[j].returnExpectedTime().hour) + ":" + str('%02d' % int(float(myB[j].returnExpectedTime().minute))), font_size=30, pos_hint={'x': 0.1, 'center_y': 0.7 - j * 0.05}))
            except:
                l.append(Label(text=str(myB[j].returnAimedTime().hour) + ":" + str('%02d' % int(float(myB[j].returnAimedTime().minute))), font_size=30,pos_hint={'x': 0.1, 'center_y': 0.7 - j * 0.05}))

        with r.canvas:
            Color(1,1,1,1)
            Line(bezier=[50, 500, 700, 500], width=2)

        for k in range(0, len(l)):
            r.add_widget(l[k])

        return r


if __name__ == '__main__':
        MyApp().run()

