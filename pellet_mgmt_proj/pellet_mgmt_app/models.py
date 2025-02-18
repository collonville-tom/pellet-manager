from django.db import models
from datetime import date
# Create your models here.

class PelletType(models.Model):
    name = models.CharField(max_length=100)
    date_achat = models.DateField(default=date.today)
    prix_unite = models.DecimalField(default=0,max_digits=5, decimal_places=2)
    poid_sac = models.DecimalField(default=15,max_digits=5, decimal_places=2)
    # on peut y inclure des validateurs
    quantite_initiale =  models.IntegerField(default=0)
    
    


class Consomation(models.Model):
    type = models.ForeignKey(PelletType, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)  
    isPerte =  models.BooleanField(default=False)


