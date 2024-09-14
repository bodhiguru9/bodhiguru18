from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .models import Package
from .serializers import PackageSerializer

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