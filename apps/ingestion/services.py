from django.db import transaction
from .models import ContentSource, RawContent

class ContentService:
    """
       Handles ingestion business logic.
    """

    @transaction.atomic
    def ingest(self, *, source_name: str, payload: dict, external_id: str = None):
        source = self._get_source(source_name)

        raw_content = RawContent.objects.create(
            source=source,
            external_id=external_id,
            payload=payload,
            status="RECEIVED",
        )
        return raw_content

    def _get_source(self, source_name: str) -> ContentSource:
        try:
            source = ContentSource.objects.get(name=source_name, is_active=True)
        except ContentSource.DoesNotExist:
            raise ValueError(f"Unknown or inactive source: {source_name}")
        return source