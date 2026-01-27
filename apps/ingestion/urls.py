from django.urls import path

from apps.ingestion.views.csv import CSVIngestionView
from apps.ingestion.views.ingestion import IngestionView

urlpatterns = [
    path('ingestion/', IngestionView.as_view(), name='ingestion-json'),
    path('csv/', CSVIngestionView.as_view(), name='ingestion-csv'),
]