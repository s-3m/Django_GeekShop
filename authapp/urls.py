from django.urls import path
import authapp.views as authapp_view

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp_view.login, name='login'),
    path('logout/', authapp_view.logout, name='logout'),
]