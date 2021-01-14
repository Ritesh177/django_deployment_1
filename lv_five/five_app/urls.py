from django.urls import path
from five_app import views

#TEMPLATE URLs
app_name='five_app'
urlpatterns=[
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),

]
