from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from hospital import views

urlpatterns = [
    path('add-resource/', views.add_resource),
]

urlpatterns = format_suffix_patterns(urlpatterns)