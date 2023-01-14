from django.urls import path 
from . import views 
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [ 
    # path('ratings', views.RatingsView.as_view()), 
   path('categories', views.CategoriesView.as_view()),
   path('categories/<str:pk>',views.cat_detail),
   
   path('menu-items', views.MenuItemsView.as_view()),
   path('menu-items/<str:pk>',views.MenuItemsViewAPI.as_view()),
   
   path('groups/manager/users',views.Groups_list),
   path('groups/manager/users/<int:pk>',views.Groups_detail),

   path('groups/delivery-crew/users',views.delivery_list),
   path('groups/delivery-crew/users/<int:pk>',views.delivery_detail),
   
   path('menu-item', views.Menu_list),
   path('menu-item/<int:pk>', views.Menu_detail),
   path('orders',views.Order_list),
   path('orders/<int:pk>',views.Order_detail),
   
   path('manager',views.managerview),
   path('api-token-auth/',obtain_auth_token),
   
   path('cart/menu-items/', views.Cart_list),
   
]