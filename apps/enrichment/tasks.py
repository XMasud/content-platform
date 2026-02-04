import logging

from celery import shared_task

from apps.enrichment.services import EnrichmentService
from apps.normalization.models import NormalizedContent

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3}
)
def enrich_content(self, normalized_content_id: int):
    logger.info(f"🔥 Enrichment started for NormalizedContent ID={normalized_content_id}")

    content = NormalizedContent.objects.filter(id=normalized_content_id).first()
    if not content:
        logger.warning(
            "⚠️ NormalizedContent not found for enrichment "
            f"(id={normalized_content_id})"
        )
        return

    if hasattr(content, "enriched"):
        return

    service = EnrichmentService()
    service.enrich_content(content)