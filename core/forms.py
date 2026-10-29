from django import forms
from .models import Contact, AgentProfile, CallRecord

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['organization', 'first_name', 'last_name', 'phone_number', 'email', 'notes']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes'}),
        }


class AgentStatusForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class SimulatedCallForm(forms.ModelForm):
    class Meta:
        model = CallRecord
        fields = ['direction', 'contact', 'notes']
        widgets = {
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Call notes...'}),
        }