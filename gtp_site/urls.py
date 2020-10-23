"""gtp_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gtp_index import views

urlpatterns = [
    # path('my_view/', views.my_view),
    # path('', views.index),
    # path('', views.HomeListView.as_view(), name='home'),
    # path('detail/<int:id>', views.detail_page),
    path('', views.index, name='home'),  # Home
    path('admin/', admin.site.urls),  # Админка
    ###########################################################################
    # path('sf/', views.ParticipantListView.as_view(), name='sf'),  # Список ДШ
    # path('sf-list/', views.sf_list, name='sf_list'),  # Список ДШ
    path('sf-list/', views.ParticipantCreateView.as_view(), name='sf_list'),  # Список ДШ
    path('sf-detail/<int:pk>', views.ParticipantDetailView.as_view(), name='detail_page'),
    # path('sf-participant-edit/<int:pk>', views.sf_participant_edit, name='sf_participant_edit'),
    path('sf-participant-edit/<int:pk>', views.ParticipantEditView.as_view(), name='sf_participant_edit'),
    # path('sf-participant-delete/<int:pk>', views.sf_participant_delete, name='sf_participant_delete'),
    path('sf-participant-delete/<int:pk>', views.ParticipantDeleteView.as_view(), name='sf_participant_delete'),
    ###########################################################################
    # path('team-list', views.team_list, name='team_list'),  # Список основной команды
    path('team-list', views.TeamMemberCreateView.as_view(), name='team_list'),  # Список основной команды
    # path('team-member-edit/<int:pk>', views.team_member_edit, name='team_member_edit'),
    path('team-member-edit/<int:pk>', views.TeamMemberEditView.as_view(), name='team_member_edit'),
    # path('team-member-delete/<int:pk>', views.team_member_delete, name='team_member_delete'),
    path('team-member-delete/<int:pk>', views.TeamMemberDeleteView.as_view(), name='team_member_delete'),
]
