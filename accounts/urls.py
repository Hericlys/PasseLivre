from django.urls import path
from accounts import views



app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('check_email/', views.check_email, name='check_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
