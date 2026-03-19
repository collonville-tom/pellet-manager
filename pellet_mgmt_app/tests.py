from django.test import TestCase, Client
from django.urls import reverse
from .models import PelletType, Consomation
from .views import StockView
from datetime import date

class PelletModelTest(TestCase):
    def setUp(self):
        self.pellet_type = PelletType.objects.create(
            name="Pellet Premium",
            date_achat=date.today(),
            prix_unite=5.50,
            poid_sac=15,
            quantite_initiale=100
        )

    def test_pellet_type_creation(self):
        """Vérifie la création d'un type de pellet avec les bonnes valeurs."""
        self.assertEqual(self.pellet_type.name, "Pellet Premium")
        self.assertEqual(float(self.pellet_type.prix_unite), 5.50)
        self.assertEqual(self.pellet_type.quantite_initiale, 100)

    def test_consommation_creation(self):
        """Vérifie la création d'une consommation liée à un type de pellet."""
        consomation = Consomation.objects.create(
            type=self.pellet_type,
            date=date.today(),
            isPerte=False
        )
        self.assertEqual(consomation.type.name, "Pellet Premium")
        self.assertFalse(consomation.isPerte)

class StockLogicTest(TestCase):
    def setUp(self):
        self.pellet_type = PelletType.objects.create(
            name="Test Stock",
            quantite_initiale=10
        )
        # 2 consommations normales
        Consomation.objects.create(type=self.pellet_type, isPerte=False)
        Consomation.objects.create(type=self.pellet_type, isPerte=False)
        # 1 perte
        Consomation.objects.create(type=self.pellet_type, isPerte=True)

    def test_stock_calculation(self):
        """Vérifie que la logique de calcul du stock dans StockView est correcte."""
        stock_view = StockView(self.pellet_type)
        stock_view.update_stat()
        
        self.assertEqual(stock_view.quantite_consomme, 2)
        self.assertEqual(stock_view.perte, 1)
        self.assertEqual(stock_view.quantite_restante, 7) # 10 - 2 - 1

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.pellet_type = PelletType.objects.create(
            name="Pellet View Test",
            quantite_initiale=50
        )

    def test_stock_page_status_code(self):
        """Vérifie que la page de stock est accessible."""
        response = self.client.get(reverse('stock'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pellet View Test")

    def test_historique_page_status_code(self):
        """Vérifie que la page d'historique est accessible."""
        response = self.client.get(reverse('historique'))
        self.assertEqual(response.status_code, 200)

    def test_add_pellet_type_post(self):
        """Vérifie l'ajout d'un type de pellet via POST."""
        data = {
            'nom': 'Nouveau Pellet',
            'prix': '6.00',
            'stock': '20',
            'poid': '15',
            'date': '2023-10-27'
        }
        response = self.client.post(reverse('stock'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PelletType.objects.filter(name='Nouveau Pellet').exists())

    def test_add_consommation_post(self):
        """Vérifie l'ajout d'une consommation via POST."""
        data = {
            'type': self.pellet_type.id,
            'date': '2023-10-27',
            'isPerte': '' # False par défaut ou vide
        }
        response = self.client.post(reverse('historique'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Consomation.objects.filter(type=self.pellet_type).count(), 1)
