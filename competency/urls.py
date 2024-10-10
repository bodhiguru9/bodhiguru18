from django.urls import path, include

from rest_framework.routers import DefaultRouter

from competency.views import CompetencyViewSet, SubCompetencyViewSet

router = DefaultRouter()
router.register(r'sub-competencies', SubCompetencyViewSet)


CompetencyViewSetRouter = DefaultRouter()

CompetencyViewSetRouter.register('', CompetencyViewSet, basename='competency')



urlpatterns = [
    path('', include(CompetencyViewSetRouter.urls)),
    path('sub-competencies/export-csv/', SubCompetencyViewSet.as_view({'get': 'export_csv'}), name='export-sub-competencies-csv'),


]
