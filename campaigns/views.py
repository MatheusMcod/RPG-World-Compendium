from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CampaignSerializer


class CampaignCreateView(APIView):
    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign_instance = serializer.save()
            return Response(CampaignSerializer(campaign_instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
