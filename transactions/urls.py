from .views import *
from django.conf                  import settings
from django.conf.urls             import url
from django.conf.urls.static      import static
from rest_framework.urlpatterns   import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Transactions")

transactions_list = TransactionViewSet.as_view({
    'get' : 'list'
})

transactions_create = TransactionViewSet.as_view({
    'post': 'create'
})

balance_retrieve = AccountViewSet.as_view({
    'get': 'retrieve'
})

urls = [
	      url(r'^$', HomeView, name='index'),
        url(r'^api/$', schema_view),
        url(r'^balance/(?P<account_number>[0-9]+)/$', balance_retrieve, name='balance-retrieve'),
        url(r'^transactions/$', transactions_create, name='transactions-create'),
        url(r'^transactions/(?P<account_number>[0-9]+)/$', transactions_list, name='transactions-list'),
        ]

urlpatterns = format_suffix_patterns(urls)
