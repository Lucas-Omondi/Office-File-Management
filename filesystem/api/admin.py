from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Expandable inline to show Counties inside Region
class CountyInline(admin.TabularInline):
    model = County
    extra = 1  # Number of empty rows
    show_change_link = True  # Allows direct editing

# Expandable inline to show Constituencies inside County
class ConstituencyInline(admin.TabularInline):
    model = Constituency
    extra = 1
    show_change_link = True

# Expandable inline to show Projects inside Constituency
class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    show_change_link = True

# Expandable inline to show Files inside Project
class FileInline(admin.TabularInline):
    model = File
    extra = 1
    show_change_link = True

# Region Admin
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CountyInline]  # Show Counties inside Region

# County Admin
@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)
    inlines = [ConstituencyInline]  # Show Constituencies inside County

# Constituency Admin
@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'county')
    list_filter = ('county',)
    search_fields = ('name',)
    inlines = [ProjectInline]  # Show Projects inside Constituency

# Project Admin (Now shows Files inside Projects)
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('rfx_number', 'name', 'contracting_company', 'contract_date', 'status', 'constituency')
    search_fields = ('name', 'rfx_number', 'contracting_company')
    list_filter = ('status', 'contract_date', 'constituency')
    # readonly_fields = ('rfx_number',)  # Prevent editing of RFX number
    inlines = [FileInline]  # Show Files inside Project

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return ['rfx_number']
        return []

    fieldsets = (
        ("Project Information", {
            'fields': ('rfx_number', 'name', 'constituency', 'status'),
        }),
        ("Contract Details", {
            'fields': ('contracting_company', 'contract_date'),
        }),
    )

# File Admin (Allows Filtering by Contractor)
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name','rfx_number', 'project', 'contracting_company', 'contract_date', 'status')
    search_fields = ('name', 'project__name','project__rfx_number', 'project__contracting_company')
    list_filter = ('project__contracting_company', 'project__status', 'project__contract_date')

    def rfx_number(self, obj):
        return obj.project.rfx_number
    rfx_number.admin_order_field = 'project__rfx_number'
    rfx_number.short_description = 'RFX Number'

    def contracting_company(self, obj):
        return obj.project.contracting_company
    contracting_company.admin_order_field = 'project__contracting_company'
    contracting_company.short_description = 'Contracting Company'

    def contract_date(self, obj):
        return obj.project.contract_date
    contract_date.admin_order_field = 'project__contract_date'
    contract_date.short_description = 'Contract Date'

    def status(self, obj):
        return obj.project.status
    status.admin_order_field = 'project__status'
    status.short_description = 'Project Status'

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_superuser")  # Show role in the list
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role",)}),  # Add role field in the admin panel
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("role",)}),
    )

# Register the custom user model
admin.site.register(User, CustomUserAdmin)