#!/usr/bin/env python3

import datetime
import xmlGet as xmlg
import xmlParse as xmlp
from bus import Buss

if __name__ == '__main__':
    xmlg.getXML();
    buses = xmlp.getBusObj()

