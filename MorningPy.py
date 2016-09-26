#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests # Brukes til å sende og hente.
import bs4 # Håndtering av XML
import xml.etree.ElementTree as ET # Alternativt bibliotek for XML-parsing

SOAP_ACTION_GET_STOP_MONITORING = "GetStopMonitoring"
NODE_MONITORED_VEHICLE_JOURNEY = "MonitoredVehicleJourney"

SIRI_SM_SERVICE = "http://st.atb.no/SMWS/SMService.svc"
SIRI_NAMESPACE = "http://www.siri.org.uk/siri"

STOP_ID = "16010011"

def getArrivalTimes(tree, location):
    """Input: XML-tree and name of bus stop. Has to be the name used in AtB's XML.
    Output: A list of existing aimed arrival times."""
    root = tree.getroot()
    StopMonitoringDelivery = root[0][0][1][0]

    # remove all non-MonitoredStopVisit-elements from tree:
    MonitoredStopVisits = []
    for deliveryElements in StopMonitoringDelivery:
        if deliveryElements.tag.find("MonitoredStopVisit") != -1:
            MonitoredStopVisits.append(deliveryElements)

    # remove all MonitoredStopVisits with incorrect location:
    ElementsOfInterest = []
    for elem in MonitoredStopVisits:
        if elem[2][6].text.find(location) != -1:
            ElementsOfInterest.append(elem)

    # create list of arrival times
    TimeTable = []
    for elem in ElementsOfInterest:
        TimeTable.append(elem[2][13][6].text)

    return TimeTable

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
    tree = ET.parse('AtB.xml')
    print(getArrivalTimes(tree, 'Pirbadet'))

if __name__ == '__main__':
    main()
