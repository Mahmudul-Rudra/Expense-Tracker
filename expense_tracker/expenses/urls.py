from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, RegisterView, current_user, ProfileUpdateView, ProfileDeleteView, get_user_profile

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('me/', get_user_profile, name = "user_profile"),
    path('profile/edit/', ProfileUpdateView.as_view(), name="edit_profile"),
    path('profile/delete/', ProfileDeleteView.as_view(), name="delete_profile"),
    path('', include(router.urls))
]
