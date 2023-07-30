from django.urls import path

from . import views

urlpatterns = [
    path('<str:score_type>/<str:position>', views.get_rankings),
    path('refresh/rankings', views.refresh_ranking_db),
    path('refresh/players', views.refresh_players_db)
]
