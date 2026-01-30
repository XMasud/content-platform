from apps.enrichment.models import EnrichedContent


class EnrichmentService:

    def enrich_content(self, normalized_payload: dict) -> dict:

        enriched= normalized_payload.copy()

        price = enriched.get('price')
        currency = enriched.get('currency')

        if price and currency:
            enriched["price_with_currency"] = f"{price} {currency}"

        enriched["enriched"] = True
        return enriched