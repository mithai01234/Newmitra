# yourapp/views.py
from rest_framework import viewsets
from .models import Ott
from .serializers import UploadedContentSerializer
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import CustomUser
from rest_framework import generics
from registration.serializers import CustomUserSerializer


class UploadedContentViewSet(viewsets.ModelViewSet):
    queryset = Ott.objects.all()
    serializer_class = UploadedContentSerializer


    def get_all_uploads(self, request):
        """
        Retrieve a list of all uploaded content.
        """
        uploads = UploadedContent.objects.all()
        serializer = self.get_serializer(uploads, many=True)
        return Response(serializer.data)
def Ottlist(request):
    registerapp=Ott.objects.all()
    context={
        'regform': registerapp



    }
    return render(request,'backend/ottlist.html',context)