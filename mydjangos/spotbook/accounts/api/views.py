from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Account
from .serializers import AccountSerializer
import json
from django.http import JsonResponse

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/account-list/',
        'Detail View': '/account-detail/<str:pk>/',
        'Create': '/account-create/',
        'Update': '/account-update/<str:pk>/',
        'Delete': '/account-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def accountList(request):
    accountList = Account.objects.all().order_by('-id')
    serializer = AccountSerializer(accountList, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def accountDetail(request, pk):
    account = Account.objects.get(id=pk)
    serializer = AccountSerializer(account, many=False)

    return Response(serializer.data)

@api_view(['POST'])
def accountCreate(request):
    payload = json.loads(request.body)

    account = Account.objects.create_user(
        email=payload['email'],
        username=payload['username']
    )

    serializer = AccountSerializer(account)
    if serializer.is_valid:
        return JsonResponse({'accounts': serializer.data})
