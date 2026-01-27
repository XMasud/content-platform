from django.db import models

from apps.ingestion.models import RawContent


class NormalizedContent(models.Model):
    """
       Stores normalized / processed data derived from RawContent(Ingestion App).
       RawContent is immutable; this model represents the output of Phase 2.
    """
    raw_content = models.OneToOneField(
        RawContent,
        on_delete=models.CASCADE,
        related_name="normalized"
    )

    normalized_payload = models.JSONField()
    status = models.CharField(max_length=20, default="SUCCESS")
    error_message = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ProcessedContent(raw_id={self.raw_content.id}, status={self.status})"