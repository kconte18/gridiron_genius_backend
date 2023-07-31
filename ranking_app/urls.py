from django.urls import path

from . import views

urlpatterns = [
    path('<str:score_type>/<str:position>', views.get_rankings),
    path('admin/refresh/rankings', views.refresh_ranking_db),
    path('admin/refresh/players', views.refresh_players_db)
]
