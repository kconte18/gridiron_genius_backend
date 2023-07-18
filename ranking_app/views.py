from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def getRankings(request):
    return HttpResponse('it works')