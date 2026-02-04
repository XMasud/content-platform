from celery import shared_task
from django.db import transaction

from apps.ingestion.models import RawContent
from apps.normalization.models import NormalizedContent
from apps.normalization.services import ContentNormalizationService
from apps.enrichment.tasks import enrich_content

import logging
logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def process_raw_content(self, raw_content_id: int):
    """
        Asynchronously processes raw content.
        Retries automatically on failure.
    """
    logger.info(f"🔥 Celery task started for RawContent ID={raw_content_id}")

    raw_content = RawContent.objects.get(id=raw_content_id)

    normalized = ContentNormalizationService().process(raw_content)

    logger.info(
        f"✅ Normalization done for RawContent ID={raw_content_id} "
        f"(NormalizedContent ID={normalized.id})"
    )

    if normalized.status != "SUCCESS":
        logger.warning(
            f"⚠️ Skipping enrichment for NormalizedContent ID={normalized.id}"
        )
        return

    logger.info(f"✅ Normalization id ={normalized.id} ")

    # ✅ Ensure DB commit before next async step
    transaction.on_commit(
        lambda: enrich_content.delay(normalized.id)
    )

    logger.info(
        f"🚀 Enrichment task scheduled for NormalizedContent ID={normalized.id}"
    )