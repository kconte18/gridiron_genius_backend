from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_rankings),
    path('refresh', views.refresh_ranking_db),
]
