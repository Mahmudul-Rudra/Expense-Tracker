from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer
from .models import ExpenseModel, Profile
from .serializers import ExpenseSerializer, UserSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

# Create your views here.
class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all();
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class ProfileDeleteView(generics.DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"detail": "User and profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    profile = request.user.profile
    return Response({
        "username": request.user.username,
        "name":profile.name,
        "email":profile.email,
        "phone":profile.phone,
        "gender":profile.gender,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = request.user.profile
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "name": profile.name,
        "email": profile.email,
        "phone": profile.phone,
        "gender": profile.gender
    })


# Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseModel.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

# # User Serializer (for registration)
# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password']
#         extra_kwargs = {'password':{'write_only':True}}
        
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# Registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.profile.name,
            "email": user.profile.email,
            "phone": user.profile.phone,
            "gender": user.profile.gender
        }, status=status.HTTP_201_CREATED)