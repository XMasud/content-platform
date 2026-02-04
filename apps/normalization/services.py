from django.db import transaction
from unicodedata import normalize
import logging

from .models import NormalizedContent
from ..ingestion.models import RawContent

logger = logging.getLogger(__name__)

class ContentNormalizationService:

    @transaction.atomic
    def process(self, raw_content: RawContent):
        logger.info(f"➡️ Processing RawContent id={raw_content.id}")

        # ✅ SAFE idempotency check
        existing = NormalizedContent.objects.filter(
            raw_content=raw_content
        ).first()

        if existing:
            logger.warning(
                f"⚠️ RawContent id={raw_content.id} already normalized "
                f"(NormalizedContent id={existing.id})"
            )
            return existing

        try:
            normalized_payload = self._normalize(raw_content)

            normalized = NormalizedContent.objects.create(
                raw_content=raw_content,
                normalized_payload=normalized_payload,
                status="SUCCESS",
            )

            logger.info(
                f"✅ NormalizedContent created for RawContent id={raw_content.id} "
                f"(NormalizedContent id={normalized.id})"
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
