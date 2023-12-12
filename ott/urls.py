# yourapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedContentViewSet,Ottlist,add_account, activate_product, deactivate_product,delete_item



urlpatterns = [
    path('api/ott', UploadedContentViewSet.as_view({'get': 'get_all_uploads'}), name='all-uploads'),
    path('api/ott/', UploadedContentViewSet.as_view({'get': 'get_video_by_id'}), name='get-video-by-id'),

    path('backend/add_ott/', add_account, name="add_accounts"),
    path('backend/ottlist/', Ottlist, name="ottlist"),
    path('backend/ottlist/activate_product/<int:id>/', activate_product, name='addcustomer/activate_product'),
    path('backend/ottlist/deactivate_product/<int:id>/', deactivate_product,name='addcustomer/deactivate_product'),
    path('backend/ottlist/delete_item/<int:myid>/', delete_item, name="addroles/delete_item"),
]
