from django.urls import path
from .views import InviteView, InviteAcceptView, CampaignView, CampaignViewList

urlpatterns = [
    path('', CampaignView.as_view(), name='campaign'),
    path('list/', CampaignViewList.as_view(), name='campaign-list'),
    path('invite/', InviteView.as_view(), name='invite'),
    path('invites/<int:invite_id>/accept/',
         InviteAcceptView.as_view(), name='invite-accept'),
]
