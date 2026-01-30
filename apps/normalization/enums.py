from django.db import models

class ProcessingStatus(models.TextChoices):
    INGESTED = "INGESTED", "Ingested"
    NORMALIZED = "NORMALIZED", "Normalized"
    ENROLLED = "ENROLLED", "Enrolled"
    VALIDATED = "VALIDATED", "Validated"
    PUBLISHED = "PUBLISHED", "Published"
    FAILED = "FAILED", "Failed"