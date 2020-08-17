"""isl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # include('features.urls', namespace= 'features')
    path('graph/', include('graph.urls')),
    #path('', include('features.urls')),

    path('', views.dashboard, name='dashboard'),
    path('data/<str:file_name>', views.data_viewer, name='data_viewer'),
    path('model/<str:file_name>', views.model_viewer, name='model_viewer'),
    path('chart/', views.chart_viewer, name='chart_viewer'),

    path('admin/', admin.site.urls),
    #path('admin/doc/', include('django.contrib.admindocs.urls')),
]
