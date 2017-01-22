from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from datetime import datetime
import nextBus as nb
import bus

def index(request):
    busGlos = nb.getBus(16011576, [5])
    busMigo = nb.getBus(16010576, [5])
    context = {}

    # improve error handling, consider _try_
    if busGlos is not None:
        context['time1'] = busGlos.getDepartureTime()
    if busMigo is not None:
        context['time2'] = busMigo.getDepartureTime()

    context['time'] = datetime.now()
    return render(request, 'mpy/index.html', context)
