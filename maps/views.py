from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from campaigns.serializers import CampaignSerializer

from .serializers import UploadedMapsSerializer
from campaigns.models import Campaigns


class MapsUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = UploadedMapsSerializer(data=request.data)

        if serializer.is_valid():
            campaign_id = request.data.get('campaign')
            campaign = Campaigns.objects.get(id=campaign_id)
            if campaign.master != request.user:
                return Response({'detail': 'Você não tem permissão para fazer upload de mapas para esta campanha.'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save(campaign=campaign)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
