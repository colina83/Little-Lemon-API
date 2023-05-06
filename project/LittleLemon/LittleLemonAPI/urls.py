from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import MenuItemView,CategoryView,ManagerLoginView

urlpatterns = [
    path("secret/", views.secret),
    path("manager/", views.manager_view),# 1. The admin can assign users to the manager group
    path('api-token-auth/', obtain_auth_token),#2. You can access the manager group with an admin token
    path('groups/manager/users',views.managers),
    path('groups/manager',views.manager_group),
    path('menu_items/', MenuItemView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('manager-login/',ManagerLoginView.as_view()),#5.- Managers Can Log in
    path('delivery-add/',views.delivery_crew),
    
    ]