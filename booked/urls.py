from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from booked import views

urlpatterns = [
    path('booked-date/', views.get_booked_detail_date),
    path('booked-range/', views.get_booked_detail_date_range),
    path('booked-history/', views.get_booked_surgery_history)
]

urlpatterns = format_suffix_patterns(urlpatterns)