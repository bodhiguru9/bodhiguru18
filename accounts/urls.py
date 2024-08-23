from django.urls import path, include
from . import views
from accounts.views import ( SendEmailConfirmationTokenAPIView,
                             UserInformationAPIVIew, confirm_email_view)


urlpatterns = [
    path('register/', views.register, name='register'),
    path('current_user/', views.current_user, name='current_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>', views.reset_password, name='reset_password'),
    path('api/me/', UserInformationAPIVIew.as_view(), name='user_information_api_view'),
    path('api/send-confirmation-email/', SendEmailConfirmationTokenAPIView.as_view(), name='send_email_confirmation_api_view'),

    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
   


] 