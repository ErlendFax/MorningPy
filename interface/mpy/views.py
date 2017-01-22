from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import nextBus as nb

def index(request):
    raw = nb.nextBus()
    #raw = 789
    m = int(raw/60)
    s = raw - m*60
    context = {'minutes': m, 'seconds': s, 'raw': raw}
    return render(request, 'mpy/index.html', context)
