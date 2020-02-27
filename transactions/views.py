from .exceptions      import LogicException
from .models          import Transaction, Account
from .serializers     import TransactionSerializer, TransactionListSerializer, AccountSerializer, AccountDetailSerializer
from django.db.models import Q
from django.http      import HttpResponseServerError, Http404
from django.shortcuts import render
from rest_framework   import viewsets, status

from rest_framework.decorators  import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response    import Response

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset           = Account.objects.all().order_by('id')
    serializer_class   = AccountDetailSerializer    

    def retrieve(self, request, account_number):
        account = Account.objects.filter(number=account_number).first()
        if account is None:
            raise Http404
        
        serializer = AccountDetailSerializer(account, many=False)
        return Response({'balance' : serializer.data })

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset           = Transaction.objects.all().order_by('id')
    serializer_class   = TransactionSerializer    
    paginator          = None

    def list(self, request, account_number):
        account = Account.objects.filter(number=account_number).first()
        if account is None:
            raise Http404
        
        queryset = Transaction.objects.filter(Q(fromAccount=account.id) | Q(toAccount=account.id))

        if 'sent' in request.GET:
            sent = self.request.GET['sent']
            queryset = Transaction.objects.filter(fromAccount=account.id)

        if 'received' in request.GET:
            sent = self.request.GET['received']
            queryset = Transaction.objects.filter(toAccount=account.id)            

        serializer = TransactionListSerializer(queryset, many=True)
        return Response({'transactions' : serializer.data })

    def create(self, request):

        try:
            data = request.data
        
            fromaccount = Account.objects.filter(number=data['fromAccount']).first()
            if fromaccount is None:
                raise Exception('Account no valid {}'.format(data['fromAccount']))

            toaccount = Account.objects.filter(number=data['toAccount']).first()
            if toaccount is None:
                raise Exception('Account no valid {}'.format(data['toAccount']))

            data['fromAccount'] = fromaccount.id
            data['toAccount']   = toaccount.id

            serializer = self.get_serializer_class()
            serializer = serializer(data=data) 

            if not serializer.is_valid(raise_exception=True):
                raise Exception('Data is not valid')

            serializer.save()            
            return Response({"status" : 200})

        except Exception as e:
            raise LogicException(detail={ "error" :  str(e) }, status_code=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def HomeView(request, format=None):
    return Response("-----")



