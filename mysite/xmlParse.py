#!/usr/bin/env python3

import datetime
import bs4
import xml.etree.ElementTree as ET
from bus import Buss

def getBusObj():
    tree = ET.parse('AtB.xml')
    root = tree.getroot()
    curChild = navigate(root)

    # Extract bus objects
    myBuses = []
    for child in curChild:
        if child.tag == "MonitoredStopVisit":
            for subChild in child:
                if subChild.tag == "MonitoredVehicleJourney":
                    myBuses.append(Buss(subChild))

    # Extract departure times
    i = 0
    j = 0
    for bus in myBuses:
        for node in bus.node:
            if node.tag == "MonitoredCall":
                for subnode in node:
                    if subnode.tag == "AimedDepartureTime":
                        time = striptime(subnode.text)
                        bus.addTime(time, False)
                        i = i + 1
                    if subnode.tag == "ExpectedDepartureTime":
                        time = striptime(subnode.text)
                        bus.addTime(time, True)
                        j = j + 1
    return myBuses

def navigate(root):
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
    return curChild

# strip time out from AtB string
# TODO: regexp to extract time
def striptime(text):
    time = text.replace("\n", "")
    time = text.replace(" ", "")
    time = text[21:29]
    h = time[0:2]
    m = time[3:5]
    s = time[6:8]
    return datetime.time(hour=int(h),minute=int(m),second=int(s))
    
