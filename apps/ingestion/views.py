from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import IngestionRequestSerializer
from .services import ContentService

class IngestionView(GenericAPIView):

    serializer_class = IngestionRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ContentService()

        try:
            raw_data = service.ingest(
                source_name=serializer.validated_data["source"],
                external_id=serializer.validated_data.get("external_id"),
                payload=serializer.validated_data["payload"],
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"id": raw_data.id},
            status=status.HTTP_201_CREATED
        )