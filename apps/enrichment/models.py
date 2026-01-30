from django.db import models

from apps.normalization.models import NormalizedContent


class EnrichedContent(models.Model):
    normalized_content = models.OneToOneField(
        NormalizedContent,
        on_delete=models.CASCADE,
        related_name="enriched_content",
    )

    enriched_payload = models.JSONField()
    status = models.BooleanField(max_length=20, default="SUCCESS")
    error_message = models.TextField(null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{EnrichedContent(norm_id={self.normalized_content.id})}"
