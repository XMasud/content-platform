from celery import shared_task

from apps.enrichment.models import EnrichedContent
from apps.enrichment.services import EnrichmentService
from apps.normalization.models import NormalizedContent


@shared_task(bind=True, autoretry_for=(Exception,), rettry_backoff=5, retry_kwargs={"max_retries": 3})
def enrich_content(self, normalized_content_id: int):
    content = NormalizedContent.objects.get(id=normalized_content_id)

    if hasattr(content, "enriched"):
        return

    service = EnrichmentService()
    enriched_payload = service.enrich_content(content.normalized_payload)

    EnrichedContent.objects.create(
        normalized_content=content,
        enriched_payload=enriched_payload
    )