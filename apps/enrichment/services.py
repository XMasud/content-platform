import logging

from django.db import transaction

from apps.enrichment.models import EnrichedContent
from apps.normalization.enums import ProcessingStatus

logger = logging.getLogger(__name__)


class EnrichmentService:

    @transaction.atomic
    def enrich_content(self, normalized_content):

        enriched, created = EnrichedContent.objects.get_or_create(
            normalized_content=normalized_content,
            defaults={
                "enriched_payload": self._enrich_payload(normalized_content),
                "status": ProcessingStatus.ENRICHED
            }
        )

        if not created:
            logger.info(
                f"Enrichment already exists for NormalizedContent {normalized_content.id}"
            )

        return enriched

    def _enrich_payload(self, normalized_content):

        data = normalized_content.normalized_payload
        content = data.get("content", {})

        enriched = {
            **data,
            "enrichment": {
                "price_eur": self._normalize_price(content),
                "keywords": self._extract_keywords(content),
                "confidence_score": 0.95
            }
        }

        return enriched

    def _normalize_price(self, content):
        price = content.get("price")
        currency = content.get("currency", "EUR")

        if price is None:
            return None

        if currency == "USD":
            return round(float(price) * 1.18, 2)

        return price

    def _extract_keywords(self, content):
        title = content.get("title", "")
        return title.lower().split()
