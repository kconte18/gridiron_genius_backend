from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_rankings),
    path('refresh/rankings', views.refresh_ranking_db),
    path('refresh/players', views.refresh_players_db)
]
