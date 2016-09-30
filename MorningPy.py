#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests # Brukes til å sende og hente.
import bs4 # Håndtering av XML
import xml.etree.ElementTree as ET # Alternativt bibliotek for XML-parsing
import time

SOAP_ACTION_GET_STOP_MONITORING = "GetStopMonitoring"
NODE_MONITORED_VEHICLE_JOURNEY = "MonitoredVehicleJourney"

SIRI_SM_SERVICE = "http://st.atb.no/SMWS/SMService.svc"
SIRI_NAMESPACE = "http://www.siri.org.uk/siri"

# Bus-stop identifier. Available at AtB's webpages.
STOP_ID = "16010576"

def getDepartureTimes(tree, busNo):
    """ Given a tree corresponding to the desired bus-stop, and line-no, this
    function will return a list of tuples (index, time_struct) corresponding to
    the buses in the given tree "tree". """
    root = tree.getroot()

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
    buses = []
    for child in curChild:
        if child.tag == "MonitoredStopVisit":
            for subChild in child:
                if subChild.tag == "MonitoredVehicleJourney":
                    buses.append(subChild)

    # Filter buses
    myBuses = []
    for bus in buses:
        for node in bus:
            if node.tag == "LineRef":
                # .text returns "polluted" text :-(
                if(node.text.find(str(busNo)) != -1):
                   myBuses.append(bus)
                break

    # Extract times (WARN: skjeten kode ahead!)
    aimedTimes = []
    expectedTimes = []

    i = 0
    j = 0
    for bus in myBuses:
        for node in bus:
            if node.tag == "MonitoredCall":
                for subnode in node:
                    if subnode.tag == "AimedDepartureTime":
                        aimedTime = subnode.text
                        aimedTime = aimedTime.replace("\n", "")
                        aimedTime = aimedTime.replace(" ", "")
                        aimedTime = aimedTime[11:19]
                        aimedTimeS = time.strptime(aimedTime, "%H:%M:%S")
                        aimedTimes.append((i, aimedTimeS))
                        i = i + 1
                    if subnode.tag == "ExpectedDepartureTime":
                        expectedTime = subnode.text
                        expectedTime = expectedTime.replace("\n", "")
                        expectedTime = expectedTime.replace(" ", "")
                        expectedTime = expectedTime[11:19]
                        expectedTimeS = time.strptime(expectedTime, "%H:%M:%S")
                        expectedTimes.append((j,expectedTimeS))
                        j = j + 1

    # TODO: Return in time-module format
    busTimes = aimedTimes + expectedTimes # smooth
    busTimes = sorted(busTimes, key=lambda tup: tup[0])

    return busTimes

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


def busStopForecast(stopId,namespace,url):

    body = getEnvelope(STOP_ID, SIRI_NAMESPACE)
    headers = {'Content-type': 'text/xml; charset=UTF-8', "SOAPAction": SOAP_ACTION_GET_STOP_MONITORING}

    response = requests.post(SIRI_SM_SERVICE, data=body, headers=headers)

    if response.status_code == 200:
        print("Success")
    else:
        print("Error code: ", end='')
        print(response.status_code)
        return

    soup = bs4.BeautifulSoup(response.content, "lxml-xml", from_encoding='UTF-8')

    print("Title:", end='')
    print(soup.find('StopPointName'))

    f = open("AtB.xml", "wb")
    f.write(soup.prettify(encoding='UTF-8',formatter='minimal')) # Lagrer en xml fil som er 'pretty'.
    f.close()

def main():
    # Uncomment line below to request new XML-data from AtB
    # busStopForecast(STOP_ID,SIRI_NAMESPACE,SIRI_SM_SERVICE)
    tree = ET.parse('AtB.xml')
    departures = getDepartureTimes(tree, 5)

    # Example: printing H:M
    for item in departures:
        print(item[1].tm_hour, ":",  item[1].tm_min)

if __name__ == '__main__':
    main()
