from django.urls import path
from requerer import views



app_name = 'requerer'

urlpatterns = [
    path('', views.home, name='home'),
    path('new_request', views.new_request, name='new_request'),
]
