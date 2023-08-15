from django.urls import path

from . import views

urlpatterns = [
    path('get/<str:score_type>/<str:position>', views.get_rankings),
    # Admin stuff
    path('refresh/rankings', views.refresh_ranking_db),
    path('refresh/players', views.refresh_players_db),
    # path('admin/login', admin.login)
    # URL FOR TESTING WITHOUT MESSING DB
    path('testing/refresh/rankings/test', views.test)
]
