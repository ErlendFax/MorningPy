#!/usr/bin/env python3

import datetime
import time
import xmlGet
import xmlParse
from bus import Buss

def timeDelta(t1, t2):
    s = t2.second - t1.second
    s += 60*(t2.minute - t1.minute)
    s += 3600*(t2.hour - t1.hour)
    return abs(s)

def getBus(busStopID, busNumber=None):
    xmlGet.getXML(busStopID)
    buses = xmlParse.getBusObj(busNumber)

    t1 = datetime.datetime.now().time()
    ret = None
    tbest = 99999
    for bus in buses:
        t2 = bus.getDepartureTime()
        if timeDelta(t1, t2) < tbest:
            ret = bus
            tbest = timeDelta(t1, t2)

    return ret

if __name__ == '__main__':
    print(getBus(16011576, [5]))
