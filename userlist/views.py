from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import CustomUser
from rest_framework import generics
from registration.serializers import CustomUserSerializer
from .serializers import CustomuSerializer
def registerlist(request):
    registerapp=CustomUser.objects.all()
    context={
        'regform': registerapp



    }
    return render(request,'backend/registerList.html',context)
class CustomUserList(generics.ListAPIView):
    serializer_class = CustomuSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

def view_item(request, myid):
    sel_regform = CustomUser.objects.get(id=myid)
    reg = CustomUser.objects.all()
    context = {
        'regform': reg,
        'sel_regform': sel_regform

    }
    return render(request, 'backend/registerview.html', context)
def activate_catagory(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 1
    banner.save()
    return redirect('userlist')  # Redirect to your banner list view

def deactivate_catagory(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 2
    banner.save()
    return redirect('userlist')  # Redirect to your banner list view
# Create your views here.
def suspend_user(request, catagory_id):
    banner = get_object_or_404(CustomUser, id=catagory_id)
    banner.status = 3
    banner.save()


    return redirect('userlist')  # Redirect to your category list view
class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
      # You can define your own permission class here if needed

    def destroy(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')

        if user_id is not None:
            try:
                user = CustomUser.objects.get(id=user_id)
                user.delete()
                return Response({"message": "User deleted successfully"}, status=204)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            return Response({"error": "User ID is required as a query parameter"}, status=400)
