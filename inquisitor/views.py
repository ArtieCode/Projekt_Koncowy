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

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        self.extra_context = {}
        active_address = None
        addresses = self.object.agencyaddress_set.all()
        for address in addresses:
            if address.address_type == 2:
                active_address = address.raw_address

        self.extra_context['active_address'] = active_address

        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

