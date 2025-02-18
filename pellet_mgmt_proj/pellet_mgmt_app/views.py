from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from pellet_mgmt_app.models import PelletType
from pellet_mgmt_app.models import Consomation

class StockView():

    def __init__(self, pelletType):
        self.id = pelletType.id
        self.name = pelletType.name
        self.date_achat = pelletType.date_achat
        self.prix_unite = pelletType.prix_unite
        self.poid_sac = pelletType.poid_sac
        self.quantite_initiale = pelletType.quantite_initiale
        self.quantite_consomme = "TBD"
        self.perte = "TBD"
        self.quantite_restante = "TBD"

    def update_stat(self):
        self.quantite_consomme = Consomation.objects.filter(type=self.id,isPerte=False).count()
        self.perte = Consomation.objects.filter(type=self.id,isPerte=True).count()
        self.quantite_restante = self.quantite_initiale - self.quantite_consomme - self.perte



def stock(request):

    if request.method == 'POST':
        # utiliser un Form pour valider les données
        nom = request.POST.get('nom')
        prix = request.POST.get('prix')
        stock = request.POST.get('stock')
        poid = request.POST.get('poid')
        date = request.POST.get('date')
        PelletType.objects.create(name=nom,
                          date_achat=date,
                          prix_unite=prix,
                          poid_sac=poid,
                          quantite_initiale=stock)

    pelletType = [StockView(obj) for obj in PelletType.objects.all() ]
    [obj.update_stat() for obj in pelletType ]
    # possiblement definir un DTO pour consolider les données manquantes
    # a constuire sur la base d'un service
    context = {
        'pelletType': pelletType,
    }

    return render(request,'stock.html',context)


def historique(request):

    if request.method == 'POST':
        # utiliser un Form pour valider les données
        type = request.POST.get('type')
        pelletTypeObject=PelletType.objects.get(pk=type)
        date = request.POST.get('date')
        isPerte = request.POST.get('isPerte')
        Consomation.objects.create(type=pelletTypeObject,
                                  date=date,
                                  isPerte=isPerte or False)

    pelletType = [StockView(obj) for obj in PelletType.objects.all() ]
    [obj.update_stat() for obj in pelletType ]
    
    consommations = Consomation.objects.all().order_by("-date")
    # possiblement definir un DTO pour consolider les données manquantes
    # a constuire sur la base d'un service
    context = {
        'pelletType': pelletType,
        'consommations': consommations
    }

    return render(request,'historique.html',context)



