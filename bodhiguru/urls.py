"""
URL configuration for bodhiguru project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import LoginViewSet
#from sean.views import DownloadFiles

def health_check(request):
    return HttpResponse('HEALTHY')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check),
    path('accounts/', include('accounts.urls')),
    #path('users/', include('users.urls')),
    path('api/token/', LoginViewSet.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #path('sean/', include('sean.urls')),
    path('industry/', include('industry.urls')),
    #path('', include('orgs.urls')),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('words/', include('words.urls')),
    
    #path('scenarios/', include('scenarios.urls')),
    #path('seanscenarios/', include('sean_scenarios.urls')),
    #path('assessments/', include('assessments.urls')),
    #path('orgs/', include('orgs.urls')),
    #path('learningcourse/', include('learningcourse.urls')),
    #path('series/', include('series.urls')),
    #path('assign/', include('assign.urls')),
    #path('saas/', include('SaaS.urls')),
    path('competency/', include('competency.urls')),
    
    #path('downloadfile/', DownloadFiles.as_view(), name='download-file')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
