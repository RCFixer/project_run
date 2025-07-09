from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.conf import settings

from .models import Run
from .serializers import RunSerializer

# Create your views here.
@api_view(['GET'])
def get_company_details(request):
    return Response(
        {
            'company_name': settings.COMPANY_NAME,
            'slogan': settings.SLOGAN,
            'contacts': settings.CONTACTS,
        },
        status=status.HTTP_200_OK
    )

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
