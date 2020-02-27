from django.core.management.base  import BaseCommand, CommandError
from random                       import randint
from transactions.models          import Account

import random
import decimal

class Command(BaseCommand):
    help = 'Property fixture'
       
    def handle(self, *args, **options):
        try:
            for i in range(10):
                item = Account.objects.create(balance=float(random.randrange(500, 100000))/100, owner=random.randint(1,10000), number=random.randint(0,10000))
                print('Account {} has been created, balance: {}'.format(item.number, item.balance))             
        except Exception as e:
            print(str(e))

