from django.contrib import admin
from .models import CustomUser, ApiKey


admin.site.register(CustomUser)
admin.site.register(ApiKey)
