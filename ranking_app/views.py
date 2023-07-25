from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

from . import services

# Create your views here.
def refresh_ranking_db(request):
    data = services.web_scrap_to_db()
    print(data)
    return HttpResponse('it worked')

def refresh_players_db(request):
    try:
        services.update_players()
        return HttpResponse("Players Updated")
    except:
        return HttpResponseServerError("Error in update_players()")

def get_rankings(request):
    return HttpResponse('it works')