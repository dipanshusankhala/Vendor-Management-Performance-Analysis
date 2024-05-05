from django.urls import path
from . import views

urlpatterns = [
    path('vendors/<str:vendor_code>/performance/', views.get_vendor_performance, name='vendor_performance'),
    path('purchase_orders/<str:po_number>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
    
]
