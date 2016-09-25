import requests # Brukes til å sende og hente.
import xml.dom.minidom # Brukes til å lage en pretty-versjon av xml-filen som lagres på disk.
import xml.etree.ElementTree as ET # Brukes til å hente elementer fra xml-filen (tror jeg).

SOAP_ACTION_GET_STOP_MONITORING = "GetStopMonitoring"
NODE_MONITORED_VEHICLE_JOURNEY = "MonitoredVehicleJourney"

SIRI_SM_SERVICE = "http://st.atb.no/SMWS/SMService.svc"
SIRI_NAMESPACE = "http://www.siri.org.uk/siri"

STOP_ID = "16010011"

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

    myXML = xml.dom.minidom.parseString(response.content) # Denne lager en xml-fil slik at vi ...
    pretty_xml_string = myXML.toprettyxml(encoding='utf-8') # ... her kan gjøre den pretty før den lagres på en fil.

    root = ET.fromstring(response.content) # Denne laget en datastruktur man kan arbeide med (tror jeg?).

    f = open("AtB.xml", "wb")
    f.write(pretty_xml_string) # Lagrer en xml fil som er 'pretty'.
    f.close()

def main():
    busStopForecast(STOP_ID,SIRI_NAMESPACE,SIRI_SM_SERVICE)

if __name__ == '__main__':
    main()


