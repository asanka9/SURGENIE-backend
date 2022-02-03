from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from team import views

urlpatterns = [
    path('team-detail/', views.get_my_team_details),
    path('create-team/', views.create_team)
]

urlpatterns = format_suffix_patterns(urlpatterns)