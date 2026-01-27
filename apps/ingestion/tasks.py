from celery import shared_task

from apps.ingestion.models import RawContent
from apps.normalization.services import ContentNormalizationService

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

    service = ContentNormalizationService()
    service.process(raw_content)
    logger.info(f"✅ Normalization done for RawContent ID={raw_content_id}")