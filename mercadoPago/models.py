from django.db import models

class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    payer_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment {self.payment_id} - {self.status}'
