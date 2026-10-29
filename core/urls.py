from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('agent-workspace/', views.agent_workspace, name='agent_workspace'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('settings/', views.organization_settings, name='organization_settings'),
    path('ai-review/', views.ai_review, name='ai_review'),
    path('calls/', views.calls, name='calls'),
    path('contacts/', views.contacts, name='contacts'),
    path('agents/', views.agents, name='agents'),
    path('api/trigger-call/', views.trigger_call, name='trigger_call'),
    path('api/twilio-token/', views.get_twilio_token, name='twilio_token'),
]