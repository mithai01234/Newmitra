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
from rest_framework.response import Response
class UploadedContentViewSet(viewsets.ModelViewSet):
    queryset = Ott.objects.filter(status=True)
    serializer_class = UploadedContentSerializer


    def get_all_uploads(self, request):
        """
        Retrieve a list of all uploaded content with status=True.
        """
        uploads = Ott.objects.filter(status=True)
        serializer = self.get_serializer(uploads, many=True)
        return Response(serializer.data)

    def get_video_by_id(self, request, ):
        video_id = request.query_params.get('ott_id')
        """
        Retrieve a specific video by ID.
        """
        try:
            video = Ott.objects.get(id=video_id, status=True)
            serializer = self.get_serializer(video)
            return Response(serializer.data)
        except Ott.DoesNotExist:
            return Response({"message": "Video not found"}, status=404)
def Ottlist(request):
    registerapp=Ott.objects.all()
    context={
        'regform': registerapp



    }
    return render(request,'backend/ottlist.html',context)
def add_account(request):
    if request.method == "POST":
        contact = Ott()
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video')

        contact.title = title
        contact.description =description
        contact.file = video_file

        contact.save()

        return render(request, 'backend/uploadott.html')
    return render(request, 'backend/uploadott.html')
def activate_product(request, id):
    banner = get_object_or_404(Ott, id=id)
    banner.status = True
    banner.save()
    return redirect('ottlist')  # Redirect to your banner list view

def deactivate_product(request, id):
    banner = get_object_or_404(Ott, id=id)
    banner.status = False
    banner.save()
    return redirect('ottlist')  # Redirect to your banner list view
def delete_item(request, myid):
    productapp = Ott.objects.get(id=myid)
    productapp.delete()
    return redirect('ottlist')
