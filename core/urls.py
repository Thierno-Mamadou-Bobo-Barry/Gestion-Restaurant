from django.urls import path
from . import views

urlpatterns = [
    path("", views.plats, name="plats"),
    path("panier/", views.panier, name="panier"),

    path("serveur/", views.serveur_dashboard, name="serveur_dashboard"),
    path("serveur/prendre/<int:commande_id>/", views.prendre_commande, name="prendre_commande"),

    path("cuisine/", views.cuisine_dashboard, name="cuisine_dashboard"),
    path("cuisine/prete/<int:commande_id>/", views.commande_prete, name="commande_prete"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
