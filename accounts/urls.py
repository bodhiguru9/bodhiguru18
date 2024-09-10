from django.urls import path, include
from . import views
from accounts.views import ( SendEmailConfirmationTokenAPIView,
                             UserInformationAPIVIew, confirm_email_view,
                             SendWelcomeEmailView, CustomTokenObtainPairView, UserUpdateView, UserListView,
                             DownloadSampleCSV, BulkUserUploadView, RegisterView,
                             DisableUserView, EnableUserView)


urlpatterns = [
    #path('register/', views.register, name='register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('current_user/', views.current_user, name='current_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
    path('api/me/', UserInformationAPIVIew.as_view(), name='user_information_api_view'),
    path('api/send-confirmation-email/', SendEmailConfirmationTokenAPIView.as_view(), name='send_email_confirmation_api_view'),

    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
    path('send-welcome-email/', SendWelcomeEmailView.as_view(), name='send-welcome-email'),
    path('check-org-validity/', views.check_org_validity, name='check-org-validity'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('bulk-upload/', BulkUserUploadAPIView.as_view(), name='bulk-user-upload'),
    path('download-sample-csv/', DownloadSampleCSV.as_view(), name='download-sample-csv'),
    path('upload-users/', BulkUserUploadView.as_view(), name='bulk-user-upload'),
    path('org-users/', UserListView.as_view(), name='user-list'),
    path('org-users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('disable-user/<int:pk>/', DisableUserView.as_view(), name='disable-user'),
    path('enable-user/<int:pk>/', EnableUserView.as_view(), name='enable-user'),

] 