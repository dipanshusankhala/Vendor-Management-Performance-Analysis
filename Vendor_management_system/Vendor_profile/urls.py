from django.urls import path
from . import views

urlpatterns = [
   
    path('vendors/create/', views.create_vendor, name='create_vendor'),  
    path('vendors/', views.list_vendors, name='list_vendors'),
    path('vendors/<str:vendor_code>', views.get_vendor, name='get_vendor'),
    path('vendors/update/<str:vendor_code>', views.update_vendor, name='update_vendor'),
    path('vendors/delete/<str:vendor_code>', views.delete_vendor, name='delete_vendor'),
]
 