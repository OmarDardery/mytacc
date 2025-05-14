from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('api/send-code/', views.send_code, name='send-code'),
    path('api/auth/', views.user_login, name='login'),
    path('api/validate-code/', views.validate_code, name='validate-code'),
    path('home', views.home, name='accountPage'),
    path('api/logout/', views.user_logout, name='logout'),
    path('api/logout/after-logout', views.index, name='index'),
    path('account/', views.account_page, name='account-page'),
    path('api/log/<str:type>', views.log, name='log'),
]