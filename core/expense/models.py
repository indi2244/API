from django.db import models

class Transactions(models.Model):
    title=models.CharField(max_length=20)
    amount= models.FloatField()
    transaction_type=models.CharField(max_length=100,choices=(("CREDIT", "CREDIT"),("DEBIT","DEBIT")))

    def save(self,*args,**kwargs):
        if self.transaction_type == "DEBIT":
            self.amount=self.amount * -1
        return super().save(*args,**kwargs)
