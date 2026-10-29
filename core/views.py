import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import Contact, AgentProfile, CallRecord, Queue, Subscription
from .forms import ContactForm, AgentStatusForm, SimulatedCallForm
from .twilio_service import make_outbound_call
import anthropic

# --- Brand Colors Helper ---
def get_brand_colors():
    return {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }

# --- CRM View ---
def dashboard(request):
    contacts = Contact.objects.all().order_by('-created_at')
    context = {
        'colors': get_brand_colors(),
        'contacts': contacts,
        'total_contacts': contacts.count(),
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
    context = {'colors': get_brand_colors(), 'form': form}
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
    context = {
        'colors': get_brand_colors(), 'form': form, 'call_form': call_form,
        'agent_profile': agent_profile, 'call_history': call_history,
    }
    return render(request, 'core/agent_workspace.html', context)

# --- Supervisor View ---
@login_required
def supervisor_dashboard(request):
    queues = Queue.objects.all()
    agents = AgentProfile.objects.all()
    context = {
        'colors': get_brand_colors(),
        'queues': queues,
        'agents': agents,
    }
    return render(request, 'core/supervisor.html', context)

# --- Organization Settings ---
@login_required
def organization_settings(request):
    subscription = Subscription.objects.first()
    context = {'colors': get_brand_colors(), 'subscription': subscription}
    return render(request, 'core/settings.html', context)

# --- Twilio Telephony ---
def trigger_call(request):
    if request.method == 'POST':
        to_number = request.POST.get('phone_number')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        if not to_number:
            return JsonResponse({'status': 'error', 'message': 'No phone number provided.'})
        result = make_outbound_call(to_number, from_number)
        return JsonResponse(result)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def get_twilio_token(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    twiml_app_sid = os.getenv('TWILIO_TWIML_APP_SID')
    if not all([account_sid, api_key, api_secret, twiml_app_sid]):
        return JsonResponse({'error': 'Twilio credentials missing. Check .env file.'}, status=500)
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VoiceGrant
    token = AccessToken(account_sid, api_key, api_secret, identity=request.user.username)
    grant = VoiceGrant(outgoing_application_sid=twiml_app_sid)
    token.add_grant(grant)
    return JsonResponse({'token': token.to_jwt()})

# --- AI Summary View ---
def ai_review(request):
    summary = None
    transcript = ""
    if request.method == 'POST':
        transcript = request.POST.get('transcript', '')
        if transcript:
            try:
                client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                prompt = f"""
                You are an AI assistant for a Contact Center. 
                Analyze the following call transcript and provide a summary.
                IMPORTANT: You must detect the language of the transcript. If it is in Arabic, reply in Arabic. If it is in English, reply in English.
                
                Format the response with:
                - Summary
                - Sentiment (Positive, Neutral, Negative)
                - Actionable Follow-up Items
                
                Transcript: {transcript}
                """
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response.content[0].text
            except Exception as e:
                summary = f"Error generating summary: {str(e)}"
                
    context = {
        'colors': get_brand_colors(),
        'summary': summary,
        'transcript': transcript,
    }
    return render(request, 'core/ai_review.html', context)


# --- DIRECTORY VIEWS ---

def calls(request):
    from .models import CallRecord
    call_history = CallRecord.objects.all().order_by('-started_at')
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/calls.html', {'colors': brand_colors, 'call_history': call_history})

def contacts(request):
    from .models import Contact
    all_contacts = Contact.objects.all().order_by('-created_at')
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/contacts.html', {'colors': brand_colors, 'contacts': all_contacts})

def agents(request):
    from .models import AgentProfile
    all_agents = AgentProfile.objects.all()
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    return render(request, 'core/agents.html', {'colors': brand_colors, 'agents': all_agents})


# --- CRM: Add Organization ---
from .forms import OrganizationForm

def add_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization created successfully!')
            return redirect('add_contact') # Send them back to the contact form to add the person
    else:
        form = OrganizationForm()
        
    brand_colors = {
        'navy': '#0A1E3D', 'blue': '#1A4B8C', 'gold': '#C9A84C',
        'white': '#FFFFFF', 'light_gray': '#F4F6F9', 'dark_gray': '#2D3748'
    }
    
    context = {
        'colors': brand_colors,
        'form': form,
    }
    return render(request, 'core/add_organization.html', context)