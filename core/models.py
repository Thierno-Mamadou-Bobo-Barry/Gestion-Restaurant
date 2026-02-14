from django.db import models
from django.conf import settings

class TableRestaurant(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero = models.IntegerField()

    def __str__(self):
        return f"Table {self.numero}"

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="plats/", null=True, blank=True)

    def __str__(self):
        return self.nom

class Panier(models.Model):
    table = models.OneToOneField(TableRestaurant, on_delete=models.CASCADE)

    def total(self):
        return sum(item.total() for item in self.items.all())

class PanierItem(models.Model):
    panier = models.ForeignKey(Panier, related_name="items", on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def total(self):
        return self.plat.prix * self.quantite

class Commande(models.Model):
    ETAT_CHOICES = [
        ("EN_ATTENTE", "En attente"),
        ("EN_PREPARATION", "En préparation"),
        ("PRETE", "Prête"),
    ]

    table = models.ForeignKey(TableRestaurant, on_delete=models.CASCADE)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="EN_ATTENTE")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande #{self.id} - Table {self.table.numero} - {self.etat}"


class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, related_name="items", on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)

    def total(self):
        return self.plat.prix * self.quantite
