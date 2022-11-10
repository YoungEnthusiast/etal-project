from django.db import models

class Subscription(models.Model):
    subscription_choices = [
		('Yearly','Yearly'),
        ('Monthly','Monthly'),
	]
    user = models.ForeignKey('account.Researcher', null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    payment_id = models.CharField(max_length=15, null=True, blank=True)
    last_payment = models.DateTimeField(null=True, blank=True)
    current_bill = models.CharField(max_length=13, null=True, blank=True)
    subscription_type = models.CharField(max_length=7, choices=subscription_choices, null=True)
    subscription_ends = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created',)
