from django.db import models


class ContentSource(models.Model):
    """
       Represents a data source (supplier API, CSV upload, internal tool).
    """
    SOURCE_TYPES = [
        ("API", "API"),
        ("FILE", "File"),
        ("MANUAL", "Manual"),
    ]

    name = models.CharField(max_length=100, unique=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RawContent(models.Model):
    """
       Stores raw payload exactly as received.
       This is immutable business-wise.
    """

    STATUS = [
        ("RECEIVED", "Received"),
        ("FAILED", "Failed"),
    ]

    source = models.ForeignKey(ContentSource, on_delete=models.PROTECT)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS, default="RECEIVED")
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source.name} - {self.external_id or self.id}"