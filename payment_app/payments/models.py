from django.db import models

class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),('completed','Completed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.id} - {self.status}'