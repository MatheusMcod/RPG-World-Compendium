from django.urls import path

from .views import (CampaignView, CampaignViewList, InviteAcceptView,
                    InviteView, JoinRequestAcceptView, JoinRequestCreateView)

urlpatterns = [
    path('', CampaignView.as_view(), name='campaign'),
    path('list/', CampaignViewList.as_view(), name='campaign-list'),
    path('invite/', InviteView.as_view(), name='invite'),
    path('invites/<int:invite_id>/response/',
         InviteAcceptView.as_view(), name='invite-response'),
    path('join/', JoinRequestCreateView.as_view(), name='join-request-create'),
    path('join/<int:request_join_id>/response/',
         JoinRequestAcceptView.as_view(), name='join-request-response'),
]
