from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

from . import services

# Create your views here.
def refresh_ranking_db(request):
    try:
        data = services.update_rankings()
        print(data)
        return HttpResponse('Rankings Updated')
    except:
        return HttpResponseServerError('Error in update_rankings()')

def refresh_players_db(request):
    try:
        services.update_players()
        return HttpResponse("Players Updated")
    except:
        return HttpResponseServerError("Error in update_players()")

def get_rankings(request):
    return HttpResponse('it works')