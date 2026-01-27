from django.db import transaction
from unicodedata import normalize
import logging

from .models import NormalizedContent
from ..ingestion.models import RawContent

logger = logging.getLogger(__name__)


class ContentNormalizationService:

    @transaction.atomic
    def process(self, raw_content: RawContent):
        """
            Entry point for normalization.
        """

        logger.info(f"➡️ Processing RawContent id={raw_content.id}")

        # Prevent duplicate processing (VERY IMPORTANT for Celery retries)
        if hasattr(raw_content, "normalized"):
            logger.warning(
                f"⚠️ RawContent id={raw_content.id} already normalized"
            )
            return raw_content.normalized

        try:
            normalized_payload = self._normalize(raw_content)

            normalized = NormalizedContent.objects.create(
                raw_content=raw_content,
                normalized_payload=normalized_payload,
                status="SUCCESS",
            )

            logger.info(
                f"✅ NormalizedContent created for RawContent id={raw_content.id}"
            )
            return normalized

        except Exception as e:
            logger.exception(
                f"❌ Normalization failed for RawContent id={raw_content.id}"
            )

            return NormalizedContent.objects.create(
                raw_content=raw_content,
                normalized_payload={},
                status="FAILED",
                error_message=str(e),
            )

    def _normalize(self, raw_content: RawContent) -> dict:
        """
        Actual transformation logic.
        Keeps it simple for now.
        """

        payload = raw_content.payload

        # Example normalization logic
        return {
            "source": raw_content.source.name,
            "external_id": raw_content.external_id,
            "content": payload,
            "metadata": {
                "ingested_at": raw_content.received_at.isoformat()
            }
        }
