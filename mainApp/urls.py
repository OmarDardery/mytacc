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
    path('api/add/<str:type>', views.add, name='log'),
    path('api/tasks_and_debts', views.get_tasks_and_debts_and_points, name='tasks-and-debts'),
    path('api/delete-task/<int:id>', views.delete_task, name='delete-task'),
    path('api/task-is-done/<int:id>', views.task_is_done, name='task-is-done'),
    path('api/pay-off-debt/<int:id>', views.pay_off_debt, name='pay-off-debt'),
    path('api/get-user', views.get_user, name='get-user'),
]