from django.contrib import admin
from deploy.models import App
from deploy.forms import AppForm


class AppAdmin(admin.ModelAdmin):
    form = AppForm
    list_display = ('name', 'version', 'plist', 'ipa',
                    'is_active', 'added_at')

admin.site.register(App, AppAdmin)
