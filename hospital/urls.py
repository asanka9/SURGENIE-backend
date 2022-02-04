from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from hospital import views

urlpatterns = [
    path('add-resource/', views.add_resource),
    path('view-resources/', views.view_resources),
    path('all-nurse/', views.all_nurse),
    path('all-surgeon/', views.all_surgeon),
    path('all-admin/', views.all_admin),
    path('all-anesthelogist/', views.all_anesthesiologist),
    path('all-trainee-surgeon/', views.all_trainee_surgeon),

]

urlpatterns = format_suffix_patterns(urlpatterns)