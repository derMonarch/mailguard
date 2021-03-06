"""mailguard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

urlpatterns = [
    path("api/v1/registrations/", include("mailguard.registration.urls")),
    path("api/v1/configurations/", include("mailguard.configuration.urls")),
    path("api/v1/tasks/", include("mailguard.tasks.urls")),
    path("api/v1/rules/", include("mailguard.rules.urls")),
]
