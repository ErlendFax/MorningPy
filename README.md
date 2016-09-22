# MorningPy
Busstider og vær, presentert enkelt for en enklere morning. 

1. Få data fra AtB.
2. Få data fra Yr.
3. Ta over verden.


## Det bartemannen sa:

Hei, du trenger i grunn bare enkel HTTP GET og POST for å få ut data.
Så en R-Pi burde kunne gjøre jobben helt greit 🙂 Raspberryen "forstår" ikke uten videre noe som helst, så du må parse XML eller JSON, men til slikt finnes det heldigvis mange biblioteker å bruke 🙂


Om stopMonitoring:

parametrene til get(...) : 
 
    public static final String SIRI_SM_SERVICE = "http://st.atb.no/SMWS/SMService.svc";
    public static final String SIRI_NAMESPACE = "http://www.siri.org.uk/siri";

og stopId, som er f.eks. "16010011" for Prinsen kino.

Jsoup.parse(...) gir deg et element du kan plukke data fra.

Men du trenger ikke RPI eller noe annet "fancy", du trenger bare kjøre en HTTP-request med den xmlen du ser der, så får du det du trenger 🙂
