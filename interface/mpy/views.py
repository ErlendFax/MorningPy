from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from datetime import datetime
import nextBus as nb
import bus

def index(request):
    busGlos = nb.getBus(16011576, [5])
    busMigo = nb.getBus(16010576, [5])
    context = {'time': datetime.now(),
               'time1': busGlos.getDepartureTime(),
               'time2': busMigo.getDepartureTime()}
    return render(request, 'mpy/index.html', context)
