from rest_framework.generics import ListAPIView
from inquisitor.models import DetectiveAgency, AgencyAddress

class NearestAgenciesAPIView(ListAPIView):
    queryset = AgencyAddress.objects.all()


    def get_queryset(self):

        q_lat = self.request.query_params.get('lat', 51.550923)
        q_lon = self.request.query_params.get('lon', 19.080392)
        q_dist = self.request.query_params.get('dist', 300)

        return DetectiveAgency.objects.filter(company_id__in=AgencyAddress.with_distance(q_lat, q_lon).filter(distance__lte=q_dist).values('owner_id'))


