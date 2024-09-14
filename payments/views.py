from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .models import Package, , PackageDetail
from .serializers import PackageSerializer, PackageDetailSerializer, OrgSerializer

import razorpay
from django.conf import settings

from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from orgss.models import Org

from django.core.mail import send_mail

# List all packages
class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

# Detail view and redirect to payment page
class PackageDetailView(generics.RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def retrieve(self, request, *args, **kwargs):
        package = self.get_object()
        # Here, redirect to your actual payments page (replace with the actual payments page URL)
        return redirect(f'/payments/{package.id}/')



# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class PackageViewSet(viewsets.ViewSet):
    """
    API to handle listing packages and processing payments.
    """
    
    # List all available packages
    def list(self, request):
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data)

    # Razorpay Payment initiation
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        package = get_object_or_404(Package, pk=pk)
        org_id = request.data.get('org_id')
        org = get_object_or_404(Org, pk=org_id)

        # Calculate the total amount (Cost + 1% tax)
        amount = int(package.cost * 1.01 * 100)  # Convert to paise for Razorpay
        
        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        # Return the order ID and amount to the front-end for further processing
        return Response({
            "razorpay_order_id": razorpay_order['id'],
            "amount": amount,
            "package": package.name,
            "org_id": org.id
        })

    # Handle payment confirmation from Razorpay
    @action(detail=False, methods=['post'])
    def payment_confirmation(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        org_id = request.data.get('org_id')
        package_id = request.data.get('package_id')

        # Verify the Razorpay signature to ensure payment is legitimate
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Get Org and Package details
            org = get_object_or_404(Org, pk=org_id)
            package = get_object_or_404(Package, pk=package_id)

            # Update Org's validity and number of logins based on the package purchased
            if package.name == 'bronze':
                org.validity = 365
                org.number_of_logins = 18
                org.package_purchased = 'Bronze'
            elif package.name == 'silver':
                org.validity = 365
                org.number_of_logins = 24
                org.package_purchased = 'Silver'
            
            org.save()

            # Create a new PackageDetail entry
            PackageDetail.objects.create(
                org=org,
                package=package,
                transaction_details=f'Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}'
            )

            # Send an email to confirm the transaction
            send_mail(
                subject='Payment Confirmation',
                message=f'Your payment for {package.name} has been confirmed. An invoice will be sent within 48 hours.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['arindam@bodhiguru.com', org.email],  # Add org's email if available
            )

            # Return success response to the front-end
            return Response({
                'message': 'Payment successful! Invoice will be shared in 48 hours.'
            }, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response({
                'error': 'Payment verification failed!'
            }, status=status.HTTP_400_BAD_REQUEST)        