from django.urls import path
from . import views
from .views import UserStatusAPIView
urlpatterns = [
    # ... your existing URL patterns ...

    # Status API endpoints
    path('status/upload/', views.upload_status, name='upload_status'),
    path('status/list/', views.list_statuses, name='list_statuses'),
    path('status/all/', views.list_all_statuses, name='list_statuses'),
    path('delete-status/', views.delete_status, name='delete-status'),
    path('api/user_status/', UserStatusAPIView.as_view(), name='user-status-api'),
    path('api/user_list/', views.StatusAPIView.as_view(), name='get-customusers'),
]
#/delete-status/?user_id=123&status_id=45