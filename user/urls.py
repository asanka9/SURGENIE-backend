from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view()),
    path('api-auth/', views.CustomAuthToken.as_view()),
    path('register/', views.registerUser),
    path('user-info/', views.userInfo),
    path('verify-token/', views.verify_token),
    path('logout/', views.verify_token),


]

urlpatterns = format_suffix_patterns(urlpatterns)