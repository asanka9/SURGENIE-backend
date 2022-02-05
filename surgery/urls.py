from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from surgery import views

urlpatterns = [
    path('predicted-results/', views.get_predicted_results),
    path('create-surgery-team/', views.create_surgery_team),
    path('create-surgery/', views.create_surgery_with_schedule),
    path('predict-time/', views.get_predicted_time),

]

urlpatterns = format_suffix_patterns(urlpatterns)