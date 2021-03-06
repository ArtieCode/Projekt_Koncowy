"""ZD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from inquisitor.views import DetectiveAgencyDetailView, DetectiveAgencyListView
from inquisitor.api_views import AgencyListAPI, AgencyManageAPI


from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'agencyadmin', AgencyManageAPI, basename='agency-manage')
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^agencja/(?P<slug>[-\w]+)/$', DetectiveAgencyDetailView.as_view(), name='agency-detail'),
    re_path(r'^$', DetectiveAgencyListView.as_view()),
    path('agencyapi', AgencyListAPI.as_view())
]
