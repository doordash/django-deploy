from django.contrib import admin
from deploy.models import App
from deploy.forms import AppForm


class AppAdmin(admin.ModelAdmin):
    form = AppForm

admin.site.register(App, AppAdmin)
