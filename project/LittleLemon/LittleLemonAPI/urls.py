from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import MenuItemView,CategoryView,ManagerLoginView

urlpatterns = [
    path("secret/", views.secret),
    path("manager/", views.manager_view),
    path('api-token-auth/', obtain_auth_token),
    path('groups/manager/users',views.managers),
    path('groups/manager',views.manager_group),
    path('menu_items/', MenuItemView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('manager-login/',ManagerLoginView.as_view()),
    path('delivery-add/',views.delivery_crew),
    
    ]