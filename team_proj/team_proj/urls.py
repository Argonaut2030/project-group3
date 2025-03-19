"""
URL configuration for team_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from contacts.views import main as contact_main
from notes.views import main as note_main
from file_manager.views import list_files


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', contact_main, name='home'),
    path('', note_main, name='notes_home'),
    path('', list_files, name='file_list'),
    path('contacts/', include('contacts.urls')),
    path('notes/', include('notes.urls')),
    path('file_manager/', include('file_manager.urls')),
    path('users/', include('users.urls')),
    path('news/', include('news.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
