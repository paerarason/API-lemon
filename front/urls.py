from django.urls import path 
from . import views 
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [    
   path('', views.home),
   path('about/', views.about),
   path('sports/', views.sports),
   path('menu/', views.result),
   path('category/', views.category),
   path('category-menu/<str:pk>',views.cat_menu,name="cat_menu"),
]