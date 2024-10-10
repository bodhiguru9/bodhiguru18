from django.urls import path, include

from rest_framework.routers import DefaultRouter

from competency.views import CompetencyViewSet, SubCompetencyViewSet, upload_csv, csv_upload_page

router = DefaultRouter()
router.register(r'sub-competencies', SubCompetencyViewSet)


CompetencyViewSetRouter = DefaultRouter()

CompetencyViewSetRouter.register('', CompetencyViewSet, basename='competency')



urlpatterns = [
    path('', include(CompetencyViewSetRouter.urls)),
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('csv-upload/', csv_upload_page, name='csv_upload_page'),  # HTML upload page
    path('sub-competencies/export-csv/', SubCompetencyViewSet.as_view({'get': 'export_csv'}), name='export-sub-competencies-csv'),


]
