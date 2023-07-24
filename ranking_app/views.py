from django.http import HttpResponse
from django.shortcuts import render

from . import services

# Create your views here.
def refresh_ranking_db(request):
    data = services.web_scrap_to_db()
    print(data)
    return HttpResponse(data)

def get_rankings(request):
    return HttpResponse('it works')