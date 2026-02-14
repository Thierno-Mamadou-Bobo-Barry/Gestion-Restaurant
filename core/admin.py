from django.contrib import admin
from .models import Plat, TableRestaurant, Panier, PanierItem, Commande, CommandeItem

admin.site.register(Plat)
admin.site.register(TableRestaurant)
admin.site.register(Panier)
admin.site.register(PanierItem)
admin.site.register(Commande)
admin.site.register(CommandeItem)

