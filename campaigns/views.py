from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Campaigns, Invite, JoinRequest
from .serializers import (CampaignSerializer, InviteConfirmSerializer,
                          InviteSerializer, JoinConfirmSerializer,
                          JoinRequestSerializer)


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

    def put(self, request):
        campaign_id = request.data.get('id')
        if not campaign_id:
            return Response({'detail': 'ID da campanha não fornecido.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            campaign = Campaigns.objects.get(id=campaign_id)
        except Campaigns.DoesNotExist:
            return Response({'detail': 'Campanha não encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

        if campaign.master != request.user:
            raise Response({'Você não tem permissão para atualizar essa campanha.'},
                           status=status.HTTP_403_FORBIDDEN)

        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            updated_campaign = serializer.save()
            return Response(CampaignSerializer(updated_campaign).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        campaign_id = self.request.query_params.get('campaign_id')
        if not campaign_id:
            return Response({'detail': 'ID da campanha não fornecido.'})

        try:
            campaign = Campaigns.objects.get(id=campaign_id)
        except Campaigns.DoesNotExist:
            return Response({'detail': 'Campanha não encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

        if campaign.master != request.user:
            return Response({'detail': 'Você não tem permissão para remover essa campanha.'},
                            status=status.HTTP_403_FORBIDDEN)

        campaign.delete()
        return Response({'detail': 'Campanha deletada com sucesso.'},
                        status=status.HTTP_204_NO_CONTENT)


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

    def delete(self, request):
        invite_id = self.request.query_params.get('invite_id')
        if not invite_id:
            return Response({'detail': 'ID do convite não fornecido.'},
                            status=status.HTTP_400_BAD_REQUEST)
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
        serializer = InviteConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            invite = Invite.objects.get(
                id=invite_id, invited_user=request.user)
        except Invite.DoesNotExist:
            return Response({'detail': 'Convite não encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

        if invite.accepted and invite.status == 'accepted':
            return Response({'detail': 'Convite já aceito.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data_status = serializer.validated_data['status']

        if data_status == 'accepted':
            invite.accepted = True
            invite.status = data_status
            invite.campaign.players.add(request.user)
        elif data_status == 'rejected':
            invite.status = data_status

        invite.save()

        return Response({'detail': 'Convite aceito!'},
                        status=status.HTTP_200_OK)


class JoinRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        join_request = JoinRequest.objects.all()
        serializer = JoinRequestSerializer(join_request, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JoinRequestSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.validated_data['campaign']
            if not campaign.isPublic:
                return Response({'detail': 'Essa campanha não é pública.'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        join_id = self.request.query_params.get('join_id')
        if not join_id:
            return Response({'detail': 'ID da solictição não fornecido.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            join_request = JoinRequest.objects.get(id=join_id)
        except JoinRequest.DoesNotExist:
            return Response({'detail': 'Solicitação não encontrado.'},
                            status=status.HTTP_404_NOT_FOUND)

        join_request.delete()
        return Response({'detail': 'Solicitação deletado com sucesso.'},
                        status=status.HTTP_204_NO_CONTENT)


class JoinRequestAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_join_id):
        serializer = JoinConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            join_request = JoinRequest.objects.get(id=request_join_id)
        except JoinRequest.DoesNotExist:
            return Response({'detail': 'Solicitação não encontrada.'},
                            status=status.HTTP_404_NOT_FOUND)

        if join_request.campaign.master != request.user:
            return Response({'detail': 'Apenas o mestre pode aceitar.'},
                            status=status.HTTP_403_FORBIDDEN)

        if join_request.accepted:
            return Response({'detail': 'Solicitação já aceita.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data_status = serializer.validated_data['status']

        if data_status == 'accepted':
            join_request.accepted = True
            join_request.status = data_status
            join_request.campaign.players.add(request.user)
        elif data_status == 'rejected':
            join_request.status = data_status

        join_request.save()
        return Response({'detail': 'Solicitação aceita.'},
                        status=status.HTTP_200_OK)
