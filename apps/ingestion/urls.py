from django.urls import path
from .views import IngestionView

urlpatterns = [
    path('ingestion/', IngestionView.as_view(), name='content-ingestion'),
]