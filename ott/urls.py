# yourapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedContentViewSet,Ottlist

router = DefaultRouter()
router.register(r'ott', UploadedContentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('backend/ottlist/', Ottlist, name="ottlist"),
]
