from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('agent-workspace/', views.agent_workspace, name='agent_workspace'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('settings/', views.organization_settings, name='organization_settings'),
    path('api/trigger-call/', views.trigger_call, name='trigger_call'),
    path('api/twilio-token/', views.get_twilio_token, name='twilio_token'),
    
    # New Directory Routes
    path('contacts/', views.contact_list, name='contact_list'),
    path('calls/', views.call_list, name='call_list'),
    path('agents/', views.agent_list, name='agent_list'),
]