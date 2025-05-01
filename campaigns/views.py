from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CampaignSerializer, InviteSerializer
from .models import Invite, Campaigns
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class CampaignViewList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        campaigns = Campaigns.objects.filter(isPublic=True)
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


class CampaignView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        campaigns = Campaigns.objects.filter(
            Q(master__id=user_id) | Q(players__id=user_id)).distinct()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign_instance = serializer.save()
            return Response(CampaignSerializer(campaign_instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        invites = Invite.objects.filter(
            Q(invited_user=user_id) | Q(invited_by=user_id))
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InviteSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.validated_data['campaign']
            if campaign.master != request.user:
                return Response({'detail': 'Apenas o mestre pode convidar jogadores.'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(invited_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, invite_id):
        try:
            invite = Invite.objects.get(id=invite_id)
        except Invite.DoesNotExist:
            return Response({'detail': 'Convite não encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

        if invite.invited_by != request.user:
            return Response({'detail': 'Você não tem permissão para remover esse convite.'},
                            status=status.HTTP_403_FORBIDDEN)

        invite.delete()
        return Response({'detail': 'Convite deletado com sucesso.'},
                        status=status.HTTP_204_NO_CONTENT)


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
