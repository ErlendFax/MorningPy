public class StopMonitoring {

    public static final String SOAP_ACTION_GET_STOP_MONITORING = "GetStopMonitoring";
    public static final String NODE_MONITORED_VEHICLE_JOURNEY = "MonitoredVehicleJourney";

    public static BusStopForecast get(String stopId, String namespace, String url) throws IOException {
        String envelope = getEnvelope(stopId, namespace);
        String xml = HttpUtil.post(SOAP_ACTION_GET_STOP_MONITORING, new URL(url), envelope);
        Elements monitoredStopVisits = Jsoup.parse(xml, "", Parser.xmlParser()).select(NODE_MONITORED_VEHICLE_JOURNEY);
        return new BusStopForecast(stopId, monitoredStopVisits);
    }

    private static String getEnvelope(String stopId, String namespace) {
        return "<S:Envelope xmlns:S='http://schemas.xmlsoap.org/soap/envelope/' xmlns:s='http://www.siri.org.uk/siri' xmlns:b='" + namespace + "'>" +
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
                "</S:Envelope>";
    }

}
