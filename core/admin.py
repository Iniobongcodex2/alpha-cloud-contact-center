from django.contrib import admin
from .models import Organization, Contact, AgentProfile, Queue, QueueMembership, Subscription

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    search_fields = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'organization')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('organization',)

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'organization', 'extension')
    list_filter = ('status', 'organization')
    search_fields = ('user__username', 'extension')

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'routing_strategy', 'created_at')
    list_filter = ('organization', 'routing_strategy')
    search_fields = ('name',)

@admin.register(QueueMembership)
class QueueMembershipAdmin(admin.ModelAdmin):
    list_display = ('queue', 'agent', 'priority', 'is_active')
    list_filter = ('queue', 'is_active')
    search_fields = ('queue__name', 'agent__user__username')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'plan', 'is_active', 'max_agents')
    list_filter = ('plan', 'is_active')
    search_fields = ('organization__name',)