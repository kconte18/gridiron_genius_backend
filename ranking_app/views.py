from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import json 

from . import services

# Create your views here.
def get_rankings(request, score_type, position):
    try:
        rankings = services.get_rankings_by_score_and_position(score_type, position)
        rankings_json = json.dumps(rankings.data)
        return HttpResponse(rankings_json, content_type='application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)

@staff_member_required   
def refresh_ranking_db(request):
    try:
        services.update_rankings()
        return HttpResponse('Rankings Updated')
    except Exception as error:
        return HttpResponseServerError(error)

@staff_member_required 
def refresh_players_db(request):
    try:
        services.update_players()
        return HttpResponse("Players Updated")
    except Exception as error:
        return HttpResponseServerError(error)
    
# VIEW FOR TESTING WITHOUT MESSING WITH DB
def test(request):
    services.test()
    return HttpResponse('ok')