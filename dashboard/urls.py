from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_dashboard, name='vendor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.logout, name='logout'),
    
    ### Notification Section ###
    path('notification/<int:pk>/view/', views.notification_redirect_view, name='notification_redirect_view'),
    ### Notification Section End ###
    
    ### Navbar Section ###
    path('navbar/create/', views.navbar_create, name='navbar_create'),
    ### Navbar Section End ###
    
    ### Dashboard Section ###
    path('dashboard/order/chart/data/', views.order_chart_data, name='order_chart_data'),
    path('dashboard/order/weekly/chart/data/', views.weekly_chart_data, name='weekly_chart_data'),
    ### Dashboard Section End ###
    
    ### Banner Section ###
    path('banner/create/', views.banner_create, name='banner_create'),
    path('banner/list/', views.banner_list, name='banner_list'),
    path('banner/<int:pk>/update/', views.banner_update, name='banner_update'),
    path('banner/<int:pk>/delete/', views.banner_delete, name='banner_delete'),
    ### Banner Section End ###
    
    ### Services Section ###
    path('services/list/', views.services_list, name='services_list'),
    path('services/create/', views.services_create, name='services_create'),
    path('services/<int:pk>/update/', views.services_update, name='services_update'),
    path('services/<int:pk>/delete/', views.services_delete, name='services_delete'),
    ### Services Section End ###
    
    ### Category Section ###
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    ### Category Section End ###
    
    ### Product Section ###
    path('product/create/', views.product_create, name='product_create'),
    path('product/list/', views.product_list_page, name='product_list'),
    path('product/data/', views.ProductList.as_view(), name='product_list_data'),   # JSON Data
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    ### Product Section End ###
    
    ### Orders Section ###
    path('orders/list/', views.orders_list, name='orders_list'),
    path('orders/data/', views.OrdersListData.as_view(), name='orders_list_data'),   # JSON Data
    path('orders/<uuid:pk>/details/', views.order_details, name='order_details'),
    ### Orders Section End ###
]