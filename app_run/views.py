from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import viewsets
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Run
from .models import User
from .models import AthleteInfo
from .models import Challenge
from .serializers import RunSerializer
from .serializers import UserSerializer
from .serializers import AthleteInfoDetailSerializer
from .serializers import AthleteInfoUpdateSerializer
from .serializers import ChallengeSerializer


class CommonPagination(PageNumberPagination):
    page_size_query_param = 'size'


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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'athlete']
    ordering_fields = ['created_at']
    pagination_class = CommonPagination

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['date_joined']
    pagination_class = CommonPagination

    def get_queryset(self):
        qs = self.queryset.filter(is_superuser=False)
        user_type = self.request.query_params.get('type', None)
        if user_type == "coach":
            qs = qs.filter(is_staff=True)
        elif user_type == "athlete":
            qs = qs.filter(is_staff=False)
        return qs

class RunStartView(APIView):
    def post(self, request, run_id):
        run_object = get_object_or_404(Run, id=run_id)
        if run_object.status in ['finished', 'in_progress']:
            data = {'error': 'Run status is not init'},
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        run_object.status = 'in_progress'
        run_object.save()
        serializer = RunSerializer(run_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RunStopView(APIView):
    def post(self, request, run_id):
        run_object = get_object_or_404(Run, id=run_id)
        if run_object.status != 'in_progress':
            data = {'error': 'Run status is not in_progress'},
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        run_object.status = 'finished'
        run_object.save()
        count_finished = Run.objects.filter(status='finished', athlete=run_object.athlete).count()
        if count_finished >= 10:
            Challenge.objects.create(full_name="Сделай 10 Забегов!", athlete=run_object.athlete)
        serializer = RunSerializer(run_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AthleteInfoView(APIView):
    def put(self, request, user_id):
        user_object = get_object_or_404(User, id=user_id)
        athlete_info, created = AthleteInfo.objects.update_or_create(user_id=user_object)
        serializer = AthleteInfoUpdateSerializer(athlete_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user_object = get_object_or_404(User, id=user_id)
        athlete_info, created = AthleteInfo.objects.get_or_create(user_id=user_object)
        serializer = AthleteInfoDetailSerializer(athlete_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChallengeView(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    def list(self, request, *args, **kwargs):
        athlete_id = request.query_params.get('athlete')

        if athlete_id:
            athlete_object = get_object_or_404(User, id=athlete_id)
            self.queryset = self.queryset.filter(athlete=athlete_object)

        return super().list(request, *args, **kwargs)
