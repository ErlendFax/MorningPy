#!/usr/bin/env python3

import datetime
import time
import xmlGet as xmlg
import xmlParse as xmlp
from bus import Buss

# helper
def timeDelta(t1, t2):
    s = t2.second - t1.second
    s += 60*(t2.minute - t1.minute)
    s += 3600*(t2.hour - t1.hour)
    return abs(s)

def nextBus():
    xmlg.getXML()
    buses = xmlp.getBusObj()

    t1 = datetime.datetime.now().time()
    lt = []
    for bus in buses:
        t2 = bus.getDepartureTimeSeconds()
        lt.append(timeDelta(t1, t2))

    # no departures?
    if not lt:
        return None

    return min(lt)

# set up loop in this block
if __name__ == '__main__':
    print(nextBus())
    time.sleep(10)
    print(nextBus())
