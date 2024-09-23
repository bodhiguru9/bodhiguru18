import razorpay
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Upgrade, Upgradedetail
from orgss.models import Org
from .serializers import UpgradeSerializer, UpgradedetailSerializer, OrgSerializer, PurchaseSerializer
from django.core.mail import send_mail

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from datetime import timedelta
from django.utils import timezone


# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
"""
class UpgradeViewSet(viewsets.ViewSet):
    
    API to handle listing packages and processing payments.
    
    
    # List all available packages
    def list(self, request):
        upgrade = Upgrade.objects.all()
        serializer = UpgradeSerializer(upgrade, many=True)
        return Response(serializer.data)

    # Razorpay Payment initiation
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        upgrade = get_object_or_404(Upgrade, pk=pk)
        org_id = request.data.get('org_id')
        org = get_object_or_404(Org, pk=org_id)

        # Calculate the total amount (Cost + 1% tax)
        amount = int(upgrade.cost * 1.01 * 100)  # Convert to paise for Razorpay
        
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
            "upgrade": upgrade.name,
            "org_id": org.id
        })

    # Handle payment confirmation from Razorpay
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def payment_confirmation(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        org_id = request.data.get('org_id')
        upgrade_id = request.data.get('upgrade_id')

        # Verify the Razorpay signature to ensure payment is legitimate
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            print(razorpay_client.utility.verify_payment_signature)

            # Get Org and Package details
            org = get_object_or_404(Org, pk=org_id)
            upgrade = get_object_or_404(Upgrade, pk=upgrade_id)

            # Update Org's validity and number of logins based on the package purchased
            if upgrade.name == 'bronze':
                org.validity = 365
                org.number_of_logins = 18
                org.package_purchased = 'Bronze'
            elif upgrade.name == 'silver':
                org.validity = 365
                org.number_of_logins = 24
                org.package_purchased = 'Silver'
            
            org.save()

            # Create a new PackageDetail entry
            Upgradedetail.objects.create(
                org=org,
                upgrade=upgrade,
                transaction_details=f'Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}'
            )

            # Send an email to confirm the transaction
            send_mail(
                subject='Payment Confirmation',
                message=f'{org.name} has paid for {upgrade.name}. An invoice will be sent within 48 hours.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['arindam@bodhiguru.com'],  # Add org's email if available
            )

            # Return success response to the front-end
            return Response({
                'message': 'Payment successful! Invoice will be shared in 48 hours.'
            }, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response({
                'error': 'Payment verification failed!'
            }, status=status.HTTP_400_BAD_REQUEST)

def payment_page(request):
    upgrade_id = request.GET.get('upgrade_id')
    upgrade = Upgrade.objects.get(pk=upgrade_id)
    amount = upgrade.cost + (upgrade.cost * 0.01)  # Adding 1% tax

    return render(request, 'payments/payment_page.html', {
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount * 100,  # Convert to paise
    })


             
"""             

class UpgradeViewSet(viewsets.ViewSet):

    def list(self, request):
        # List all available packages
        upgrades = Upgrade.objects.all()
        serializer = UpgradeSerializer(upgrades, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        # Initiate the payment for a specific upgrade
        upgrade = get_object_or_404(Upgrade, pk=pk)
        org_id = request.data.get('org_id')
        org = get_object_or_404(Org, pk=org_id)  # Fetch the Org from orgss

        if upgrade.name == 'Package 9':
            # Check if the org has Bronze or Silver package
            if org.package_purchased not in ['Bronze', 'Silver']:
                return Response({'error': 'You need to have Bronze or Silver package before purchasing Package 9.'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate additional logins for Package 9
            number_of_packs = request.data.get('number_of_packs', 1)
            additional_logins = number_of_packs * 9
            cost = int(upgrade.cost * number_of_packs * 1.01 * 100)  # Cost with 1% tax

        else:
            # Calculate for Bronze or Silver package purchases
            additional_logins = 0
            cost = int(upgrade.cost * 1.01 * 100)

        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": cost,
            "currency": "INR",
            "payment_capture": "1"
        })

        # Return the order ID and amount to the front-end for further processing
        return Response({
            "razorpay_order_id": razorpay_order['id'],
            "amount": cost,
            "upgrade": upgrade.name,
            "additional_logins": additional_logins,
            "org_id": org.id
        })

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def payment_confirmation(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')
        org_id = request.data.get('org_id')
        upgrade_id = request.data.get('upgrade_id')

        # Verify the Razorpay signature to ensure payment is legitimate
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Get Org and Upgrade (Package) details
            org = get_object_or_404(Org, pk=org_id)
            upgrade = get_object_or_404(Upgrade, pk=upgrade_id)

            # Check for existing valid Bronze or Silver packages
            if upgrade.name in ['bronze', 'silver']:
                # Update Org's validity and number of logins based on the package purchased
                if upgrade.name == 'bronze':
                    org.validity = 365  # Keep validity as 365 days
                    org.number_of_logins = 18
                    org.package_purchased = 'Bronze'
                elif upgrade.name == 'silver':
                    org.validity = 365  # Keep validity as 365 days
                    org.number_of_logins = 24
                    org.package_purchased = 'Silver'
                
                org.save()

            elif upgrade.name == 'Package 9':
                # Check if the org already has Bronze or Silver package
                if org.package_purchased in ['Bronze', 'Silver']:
                    # Calculate additional logins
                    number_of_packs = request.data.get('number_of_packs', 1)
                    additional_logins = number_of_packs * 9  # Each Package 9 adds 9 logins per pack
                    org.number_of_logins += additional_logins  # Add logins to existing ones
                    
                    # Do not change validity, but set expires_on for additional logins
                    package_9_expiry = org.expires_on  # Keeping the validity unchanged (365 days)
                    
                    # Create a new Upgradedetail entry for Package 9
                    Upgradedetail.objects.create(
                        org=org,
                        upgrade=upgrade,
                        transaction_details=f'Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}',
                        additional_logins=additional_logins,
                        expires_on=package_9_expiry
                    )
                else:
                    # Prevent purchase if Bronze or Silver isn't already purchased
                    return Response({
                        'error': 'You must purchase Bronze or Silver before buying Package 9.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Send a payment confirmation email
            send_mail(
                subject='Payment Confirmation',
                message=f'{org.name} has paid for {upgrade.name}. An invoice will be sent within 48 hours.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['arindam@bodhiguru.com'],  # Add org's email if needed
            )

            # Return success response
            return Response({
                'message': 'Payment successful! Invoice will be shared in 48 hours.'
            }, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response({
                'error': 'Payment verification failed!'
            }, status=status.HTTP_400_BAD_REQUEST)