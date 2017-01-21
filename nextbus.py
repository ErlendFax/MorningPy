#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Vennligst ikke fjern linjene over. De blir lest av shell og interpreter.

import bs4 # Håndtering av XML
import xml.etree.ElementTree as ET
import datetime
import getxml

class Buss:
    def __init__(self, node):
        self.node = node
        # avoid undefined behaviour if RT is unavailable
        self.expectedTime = None

    def addAimedTime(self,aimedTime):
        self.aimedTime = aimedTime

    def addExpectedTime(self, expectedTime):
        # consider adding here
        self.expectedTime = expectedTime

    def getExpectedUntilDeparture(self):
        if self.expectedTime == None:
            return None

        now = datetime.datetime.now()
        expected = datetime.datetime.combine(now, self.expectedTime)
        return expected - now


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
    """ Parse XML, create bus objects """

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
                            expectedTimeHour = dt_obj.hour
                            expectedTimeMin = dt_obj.minute
                            expectedTimeSec = dt_obj.second
                            expectedTime = datetime.time(expectedTimeHour,
                                                         expectedTimeMin,
                                                         expectedTimeSec)
                            bus.addExpectedTime(expectedTime)
                            j = j + 1
    return myBuses

def mainRun():
    tree = ET.parse('AtB.xml')
    busObjs = getBusObj(tree)
    print("Line\tDisp\tDeparting in")
    for bus in busObjs:
        if bus.getExpectedUntilDeparture() != None:
                print(bus.getLine(),'\t',bus.getDisplay(),'\t', bus.getExpectedUntilDeparture())
    return busObjs

if __name__ == '__main__':
    mainRun()

