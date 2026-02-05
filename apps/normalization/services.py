from django.db import transaction
import logging

from jsonschema import ValidationError

from .enums import ProcessingStatus
from .models import NormalizedContent
from .schemas.normalized_content import NormalizedContentSchema
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

        normalized_payload = self._normalize(raw_content)

        try:
            validated = NormalizedContentSchema(**normalized_payload)

        except ValidationError as e:
            logger.info(f"NormalizedContentSchema validation failed: {e}")

            return NormalizedContent.objects.create(
                raw_content=raw_content,
                normalized_payload={},
                status=ProcessingStatus.FAILED,
                error_message=str(e),
            )

        return NormalizedContent.objects.create(
            raw_content=raw_content,
            normalized_payload=validated.model_dump(mode="json"),
            status=ProcessingStatus.NORMALIZED,
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
