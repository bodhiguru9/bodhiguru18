from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feedback
from .serializers import FeedbackSerializer
from django.core.mail import send_mail
from django.conf import settings

class FeedbackView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send email notification
            email_subject = 'New Feedback Submitted'
            email_message = f"Email: {serializer.validated_data['email']}\n" \
                            f"Contact Number: {serializer.validated_data['contact_number']}\n" \
                            f"Description:\n{serializer.validated_data['description']}"

            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['arindam@bodhiguru.com'],
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)