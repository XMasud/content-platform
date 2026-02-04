from django.db import models

from apps.normalization.models import NormalizedContent
from apps.normalization.enums import ProcessingStatus


class EnrichedContent(models.Model):
    normalized_content = models.OneToOneField(
        NormalizedContent,
        on_delete=models.CASCADE,
        related_name="enriched",
    )

    enriched_payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=ProcessingStatus.choices,
        default=ProcessingStatus.ENRICHED
    )

    error_message = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EnrichedContent(norm_id={self.normalized_content.id}, status={self.status})"
