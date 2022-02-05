from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from booked import views

urlpatterns = [
    path('booked-date/', views.get_booked_detail_date),
    path('booked-range/', views.get_booked_detail_date_range),
    path('booked-history/', views.get_booked_surgery_history),
    path('calender-date/', views.get_calender_with_date),
    path('calender-date-range/', views.get_calender_with_date_range)

]

urlpatterns = format_suffix_patterns(urlpatterns)