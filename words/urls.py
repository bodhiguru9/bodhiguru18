from django.urls import path, include

from rest_framework.routers import DefaultRouter

from words.views import ProductView, NegativeWordsViewSet, PowerWordsViewSet

PowerWordViewSetRouter = DefaultRouter()
NegativeWordViewSetRouter = DefaultRouter()

PowerWordViewSetRouter.register("", PowerWordsViewSet, basename="power_word")
NegativeWordViewSetRouter.register("", NegativeWordsViewSet, basename="negative_word")

urlpatterns = [
    path('bulk_create_word/', ProductView.as_view(), name='bulk-create'),
    path("power_words/", include(PowerWordViewSetRouter.urls), name='power_word'),
    path("negative_words/", include(NegativeWordViewSetRouter.urls), name='negative_word')
]
