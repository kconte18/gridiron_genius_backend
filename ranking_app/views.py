from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

import json 

from . import services

# Create your views here.
def get_rankings(request, score_type, position):
    try:
        rankings = services.get_rankings_by_score_and_position(score_type, position)
        rankings_json = json.dumps(rankings.data)
        return HttpResponse(rankings_json, content_type='application/json')
    except:
        return HttpResponseServerError("Error in get_rankings")
    
def refresh_ranking_db(request):
    try:
        services.update_rankings()
        return HttpResponse('Rankings Updated')
    except:
        return HttpResponseServerError('Error in update_rankings()')

def refresh_players_db(request):
    try:
        services.update_players()
        return HttpResponse("Players Updated")
    except:
        return HttpResponseServerError("Error in update_players()")
    
# TEMP VIEW FOR FINDING AVG, WILL BE UNDER refresh_ranking_db
def get_rankings_avg(request):
    services.get_rankings_avg()
    return HttpResponse("Good")