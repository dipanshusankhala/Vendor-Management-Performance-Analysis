from django.urls import path
from . import views

urlpatterns = [
    path('purchase_orders/create/', views.create_purchase_order, name='create_purchase_order'),
    path('purchase_orders/', views.list_purchase_orders, name='list_purchase_orders'),
    path('purchase_orders/<str:po_number>/', views.get_purchase_order, name='get_purchase_order'),
    path('purchase_orders/update/<str:po_number>/', views.update_purchase_order, name='update_purchase_order'),
    path('purchase_orders/delete/<str:po_number>/', views.delete_purchase_order, name='delete_purchase_order'),
]