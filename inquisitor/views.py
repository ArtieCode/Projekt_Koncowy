from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from inquisitor.models import DetectiveAgency

class DetectiveAgencyListView(ListView):
    model = DetectiveAgency
    paginate_by = 100
    template_name = 'basic_list.html'

class DetectiveAgencyDetailView(DetailView):
    model = DetectiveAgency
    template_name = 'agency_detail.html'

