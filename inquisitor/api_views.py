from rest_framework.generics import ListAPIView
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from inquisitor.permissions import IsOwnerOrReadOnly
from inquisitor.models import DetectiveAgency, AgencyAddress
from inquisitor.serializers import AgencySerializer

class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    pass


class AgencyListAPI(ListAPIView):
    queryset = DetectiveAgency.objects.all()
    serializer_class = AgencySerializer

    def __init__(self):
        self.address_cache = {}
        super().__init__()


    def get_queryset(self):

        q_lat = self.request.query_params.get('lat', 51.550923)
        q_lon = self.request.query_params.get('lon', 19.080392)
        q_dist = self.request.query_params.get('dist', 500)
        queryset_addresses = AgencyAddress.\
            with_distance(q_lat, q_lon).\
            filter(distance__lte=q_dist).\
            order_by('distance').\
            select_related('owner')

        self.address_cache = {}
        for address in queryset_addresses:
            if address.owner.company_id not in self.address_cache:
                address_list = [address.raw_address]
                interim_dict = {address.owner.company_id: address_list}
                self.address_cache.update(interim_dict)
            else:
                self.address_cache[address.owner.company_id].append(address.raw_address)

        queryset_agencies = DetectiveAgency.objects.\
            filter(company_id__in=self.address_cache.keys())

        return queryset_agencies



class AgencyManageAPI(RetrieveUpdateViewSet):
    queryset = DetectiveAgency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    lookup_field = 'company_id'





