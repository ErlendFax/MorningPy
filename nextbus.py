#!/usr/bin/env python3

import datetime
import xmlGet as xmlg
import xmlParse as xmlp
from bus import Buss

def timeDelta(t1, t2):
    s = t2.second - t1.second
    s += 60*(t2.minute - t1.minute)
    s += 3600*(t2.hour - t1.hour)
    return abs(s)

if __name__ == '__main__':
    xmlg.getXML();
    buses = xmlp.getBusObj()

    times = []
    t1 = datetime.datetime.now().time()
    for bus in buses:
        t2 = bus.getDepartureTimeSeconds()
        times.append(timeDelta(t1, t2))

    print(min(times))
