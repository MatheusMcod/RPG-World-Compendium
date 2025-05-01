from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CampaignSerializer, InviteSerializer
from .models import Invite
from rest_framework.permissions import IsAuthenticated


class CampaignCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign_instance = serializer.save()
            return Response(CampaignSerializer(campaign_instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InviteSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.validated_data['campaign']
            if campaign.master != request.user:
                return Response({'detail': 'Apenas o mestre pode convidar jogadores.'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(invited_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invite_id):
        try:
            invite = Invite.objects.get(
                id=invite_id, invited_user=request.user)
        except Invite.DoesNotExist:
            return Response({'detail': 'Convite não encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

        if invite.accepted:
            return Response({'detail': 'Convite já aceito.'},
                            status=status.HTTP_400_BAD_REQUEST)

        invite.accepted = True
        invite.save()
        invite.campaign.players.add(request.user)
        return Response({'detail': 'Convite aceito!'},
                        status=status.HTTP_200_OK)
