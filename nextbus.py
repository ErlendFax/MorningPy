#!/usr/bin/env python3

import bs4 # Håndtering av XML
import xml.etree.ElementTree as ET
import datetime
import getxml
from bus import Buss

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

if __name__ == '__main__':
    getxml.getXML();
    tree = ET.parse('AtB.xml')
    busObjs = getBusObj(tree)

