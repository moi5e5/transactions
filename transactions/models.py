from django.conf 		      import settings
from django.contrib           import messages
from django.db 				  import models
from django.db.models.signals import pre_save, post_save
from django.dispatch          import receiver

class BaseModel(models.Model):
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Account(BaseModel):
	balance = models.DecimalField(max_digits=20, decimal_places=2, null=False)
	number  = models.IntegerField(null=False)
	owner   = models.IntegerField(null=False)

	def account(self):
		return self.number

	def __str__(self):
		return str(self.number)

class Transaction(BaseModel):
	fromAccount  = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_from')
	toAccount    = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_to')
	amount       = models.DecimalField(max_digits=6, decimal_places=2, null=False)

	def fromaccount(self):
		return self.fromAccount.number

	def toaccount(self):
		return self.toAccount.number		


def handle_pre_validations(sender, **kwargs):
	instance  = kwargs['instance']
	if type(instance) is Transaction:
		future_balace = instance.fromAccount.balance - instance.amount
		if future_balace <= settings.MINIMUM_ALLOWED:
			raise Exception('The account balance would be reached minimum allowed.')

def handle_post_validations(sender, **kwargs):
	
	instance    = kwargs['instance']
	
	if type(instance) is Transaction:
		fromAccount = instance.fromAccount
		toAccount   = instance.toAccount

		currentFromBalance = fromAccount.balance
		currentToBalance   = toAccount.balance
		fromAccountBalance = fromAccount.balance - instance.amount
		toAccountBalance   = toAccount.balance + instance.amount	

	
		try:
			fromAccount.balance = fromAccountBalance
			toAccount.balance   = toAccountBalance

			fromAccount.save()
			toAccount.save()

		except Exception as e:
			#rollback transactions
			fromAccount.balance = currentFromBalance
			toAccount.balance   = currentToBalance

			fromAccount.save()
			toAccount.save()

			instance.delete()

			raise Exception('there\'s an error in the transaction. {}'.format(str(e)))

pre_save.connect(handle_pre_validations, dispatch_uid='validate_pre')
post_save.connect(handle_post_validations, dispatch_uid='validate_post')
