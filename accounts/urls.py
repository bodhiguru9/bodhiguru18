from django.urls import path, include
from . import views
from accounts.views import ( SendEmailConfirmationTokenAPIView,
                             UserInformationAPIVIew, confirm_email_view,
                             SendWelcomeEmailView, CustomTokenObtainPairView, UserUpdateView, UserListView,
                            RegisterView, AccountViewSet, PasswordResetRequestView, PasswordResetConfirmView,
                             DisableUserView, EnableUserView)
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')



urlpatterns = [
    #path('register/', views.register, name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('current_user/', views.current_user, name='current_user'),
    
    path('api/me/', UserInformationAPIVIew.as_view(), name='user_information_api_view'),
    path('api/send-confirmation-email/', SendEmailConfirmationTokenAPIView.as_view(), name='send_email_confirmation_api_view'),

    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
    path('send-welcome-email/', SendWelcomeEmailView.as_view(), name='send-welcome-email'),
    path('check-org-validity/', views.check_org_validity, name='check-org-validity'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('org-users/', UserListView.as_view(), name='user-list'),
    path('org-users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('disable-user/<int:pk>/', DisableUserView.as_view(), name='disable-user'),
    path('enable-user/<int:pk>/', EnableUserView.as_view(), name='enable-user'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('', include(router.urls)),

] 