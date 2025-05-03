from django.urls import path

from .views import (CampaignView, CampaignViewList, InviteAcceptView,
                    InviteView, JoinRequestAcceptView, JoinRequestView)

urlpatterns = [
    path('', CampaignView.as_view(), name='campaign'),
    path('list/', CampaignViewList.as_view(), name='campaign-list'),
    path('invite/', InviteView.as_view(), name='invite'),
    path('invite/<int:invite_id>/response/',
         InviteAcceptView.as_view(), name='invite-response'),
    path('join/', JoinRequestView.as_view(), name='join-request-create'),
    path('join/<int:request_join_id>/response/',
         JoinRequestAcceptView.as_view(), name='join-request-response'),
]
