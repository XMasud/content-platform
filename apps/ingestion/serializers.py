from rest_framework import serializers

class IngestionRequestSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=100)
    external_id = serializers.CharField(
        max_length=100, required=False, allow_null=True
    )
    payload = serializers.JSONField()

    def validate_payload(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Payload must be a JSON object")
        return value