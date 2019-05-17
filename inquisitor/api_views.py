from rest_framework.generics import ListAPIView
from rest_framework import mixins, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from inquisitor.permissions import IsOwnerOrReadOnly
from inquisitor.models import DetectiveAgency, AgencyAddress, ReferenceCity
from inquisitor.serializers import AgencySerializer
from urllib import parse


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



        req_lat = self.request.query_params.get('lat',)
        req_lon = self.request.query_params.get('lon',)
        req_dist = self.request.query_params.get('dist',)
        q_near = self.request.query_params.get('near')
        if q_near:
            q_near_encoded = self.request.query_params.get('near')
            q_near = parse.unquote(q_near_encoded)
            near_city = ReferenceCity.objects.filter(city__unaccent=q_near).first()
            if near_city:
                req_lat = near_city.geocoding_latitude
                req_lon = near_city.geocoding_longitude
                req_dist = 20


        queryset_addresses = AgencyAddress.\
            with_distance(req_lat, req_lon).\
            filter(distance__lte=req_dist).\
            order_by('distance').\
            select_related('owner')

        if not queryset_addresses.exists():
            queryset_addresses = AgencyAddress. \
                with_distance(req_lat, req_lon). \
                filter(distance__lte=2*req_dist). \
                order_by('distance'). \
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

        print(self.address_cache)
        return queryset_agencies



class AgencyManageAPI(RetrieveUpdateViewSet):
    queryset = DetectiveAgency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    lookup_field = 'company_id'





