#!/usr/bin/env python3
import time
import nextBus as nb


while True:
    t = nb.nextBus()
    
    if t == None:
        m = "??"
        s = "??"
    else:
        m = t%60
        s = t-m*60

    print(m)
    print(s)
    with open('index.html', 'r') as file:
        data = file.readlines()

    data[20] = '<span class="minutes">'+ m + '</span>\n'
    data[24] = '<span class="seconds">'+ s + '</span>\n'

    # debugging
    #i = 0
    #for line in data:
    #    print(i, line)
    #    i = i + 1

    with open('index.html', 'w') as file:
        file.writelines(data)

    time.sleep(30)

