"""
URL configuration for AI_code_healer project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),  # Include the web app's URLs
]
