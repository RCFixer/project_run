from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Run
from .models import User
from .models import STATUS
from .serializers import RunSerializer
from .serializers import UserSerializer

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
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        qs = self.queryset.filter(is_superuser=False)
        user_type = self.request.query_params.get('type', None)
        if user_type == "coach":
            qs = qs.filter(is_staff=True)
        elif user_type == "athlete":
            qs = qs.filter(is_staff=False)
        return qs

class RunStartView(APIView):
    def patch(self, request, run_id):
        run_object = get_object_or_404(Run, id=run_id)
        if run_object.status in ['finished', 'in_progress']:
            data = {'error': 'Run status is not init'},
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        run_object.status = 'in_progress'
        run_object.save()
        serializer = RunSerializer(run_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RunStopView(APIView):
    def patch(self, request, run_id):
        run_object = get_object_or_404(Run, id=run_id)
        if run_object.status != 'in_progress':
            data = {'error': 'Run status is not in_progress'},
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        run_object.status = 'finished'
        run_object.save()
        serializer = RunSerializer(run_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
