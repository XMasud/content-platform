import logging

from django.db import transaction

from apps.enrichment.models import EnrichedContent
from apps.normalization.enums import ProcessingStatus

logger = logging.getLogger(__name__)

class EnrichmentService:

    @transaction.atomic
    def enrich_content(self, normalized_payload):

        enriched, created = EnrichedContent.objects.get_or_create(
            normalized_content=normalized_payload,
            defaults={
                "enriched_payload": self._enrich_payload(normalized_payload),
                "status": ProcessingStatus.ENRICHED
            }
        )

        if not created:
            logger.info(
                f"Enrichment already exists for NormalizedContent {normalized_payload.id}"
            )

        return enriched

    def _enrich_payload(self, normalized_payload):

        data = normalized_payload.normalized_payload

        enriched = {
            **data,
            "price_eur": self._normalize_price(data),
            "keywords": self._extract_keywords(data),
            "confidence_score": 0.95
        }

        return enriched

    def _normalize_price(self, data):
        price = data.get("price")
        currency = data.get("currency","EUR")

        if price is None:
            return None

        if currency == "USD":
            return round(float(price)*1.18, 2)

        return price

    def _extract_keywords(self, data):
        title = data.get("title", "")
        return title.lower().split()