from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Main App
    path('', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('add-organization/', views.add_organization, name='add_organization'),
    path('agent-workspace/', views.agent_workspace, name='agent_workspace'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('settings/', views.organization_settings, name='organization_settings'),
    path('ai-review/', views.ai_review, name='ai_review'),
    
    # Directories
    path('calls/', views.calls, name='calls'),
    path('contacts/', views.contacts, name='contacts'),
    path('agents/', views.agents, name='agents'),
    
    # APIs & Exports
    path('api/trigger-call/', views.trigger_call, name='trigger_call'),
    path('api/twilio-token/', views.get_twilio_token, name='twilio_token'),
    path('export-calls/', views.export_calls_csv, name='export_calls'),
]