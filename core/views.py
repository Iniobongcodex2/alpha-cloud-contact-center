import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant

from .models import Contact, AgentProfile, CallRecord, Subscription
from .forms import ContactForm, AgentStatusForm, SimulatedCallForm
from .twilio_service import make_outbound_call

# --- CRM View ---
def dashboard(request):
    contacts = Contact.objects.all().order_by('-created_at')
    total_contacts = contacts.count()
    
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'contacts': contacts,
        'total_contacts': total_contacts,
    }
    return render(request, 'core/dashboard.html', context)

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact was added successfully!')
            return redirect('dashboard')
    else:
        form = ContactForm()
        
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'form': form,
    }
    return render(request, 'core/add_contact.html', context)

# --- Agent Workspace View ---
@login_required
def agent_workspace(request):
    agent_profile, created = AgentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'update_status' in request.POST:
        form = AgentStatusForm(request.POST, instance=agent_profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Status updated to {agent_profile.status}!')
            return redirect('agent_workspace')
            
    elif request.method == 'POST' and 'make_call' in request.POST:
        call_form = SimulatedCallForm(request.POST)
        if call_form.is_valid():
            call = call_form.save(commit=False)
            call.agent = agent_profile
            if call.contact:
                call.organization = call.contact.organization
            call.status = 'Completed'
            call.duration_seconds = 120
            call.save()
            messages.success(request, 'Simulated call recorded successfully!')
            return redirect('agent_workspace')
    else:
        form = AgentStatusForm(instance=agent_profile)
        call_form = SimulatedCallForm()
        
    call_history = CallRecord.objects.filter(agent=agent_profile).order_by('-started_at')
        
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'form': form,
        'call_form': call_form,
        'agent_profile': agent_profile,
        'call_history': call_history,
    }
    return render(request, 'core/agent_workspace.html', context)

# --- Twilio Telephony Integration ---
def get_twilio_token(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    twiml_app_sid = os.getenv('TWILIO_TWIML_APP_SID')

    if not all([account_sid, api_key, api_secret, twiml_app_sid]):
        return JsonResponse({'error': 'Twilio credentials missing. Check .env file.'}, status=500)

    token = AccessToken(account_sid, api_key, api_secret, identity=request.user.username)
    grant = VoiceGrant(outgoing_application_sid=twiml_app_sid)
    token.add_grant(grant)

    return JsonResponse({'token': token.to_jwt()})

def trigger_call(request):
    if request.method == 'POST':
        to_number = request.POST.get('phone_number')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not to_number:
            return JsonResponse({'status': 'error', 'message': 'No phone number provided.'})
            
        result = make_outbound_call(to_number, from_number)
        return JsonResponse(result)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# --- STAGE 7: SAAS SETTINGS ---
def organization_settings(request):
    subscription = Subscription.objects.first()
    
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'subscription': subscription,
    }
    return render(request, 'core/settings.html', context)

# --- STAGE 6: SUPERVISOR DASHBOARD ---
from .models import Queue, AgentProfile

def supervisor_dashboard(request):
    queues = Queue.objects.all()
    agents = AgentProfile.objects.all()
    
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'queues': queues,
        'agents': agents,
    }
    return render(request, 'core/supervisor.html', context)


# --- STAGE 8: AI SUMMARIES ---
from .ai_service import generate_call_summary

def ai_review(request):
    summary = None
    transcript = ""
    
    if request.method == 'POST':
        transcript = request.POST.get('transcript', '')
        if transcript:
            summary = generate_call_summary(transcript)
            
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'transcript': transcript,
        'summary': summary,
    }
    return render(request, 'core/ai_review.html', context)


# --- DIRECTORY VIEWS ---
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/contacts.html', {'colors': brand_colors, 'contacts': contacts})

def call_list(request):
    calls = CallRecord.objects.all().order_by('-started_at')
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/calls.html', {'colors': brand_colors, 'calls': calls})

def agent_list(request):
    agents = AgentProfile.objects.all()
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/agents.html', {'colors': brand_colors, 'agents': agents})