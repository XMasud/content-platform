import csv

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.models import ContentSource, RawContent
from ..tasks import process_raw_content


class CSVIngestionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        source_name = request.data.get("source")

        if not file or not source_name :
            return Response({"error": "File and source are required."}, status=400)

        source = ContentSource.objects.get(name=source_name, is_active=True)

        reader = csv.DictReader(
            file.read().decode("utf-8").splitlines()
        )

        count = 0
        for row in reader:
            raw = RawContent.objects.create(
                external_id=row["external_id"],
                source=source,
                payload=row,
                status="RECEIVED",
            )
            process_raw_content.delay(raw.id)
            count += 1
        return Response(
            {"rows_ingested": count},
            status=status.HTTP_202_ACCEPTED
        )