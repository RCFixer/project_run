from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def get_company_details(request):
    return Response(
        {
            'company_name': 'Бегун бегуныч',
            'slogan': 'Бегаем шустро...как пуля!',
            'contacts': 'Город Майами, улица Дуэйн Скала Джонсон, дом 5'
        },
        status=status.HTTP_200_OK
    )