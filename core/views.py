from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required


from .models import (
    Plat,
    Panier,
    PanierItem,
    TableRestaurant,
    Commande,
    CommandeItem,
)


# ==========================
# PAGE PLATS (TABLE)
# ==========================
@login_required
def plats(request):
    # (Optionnel) bloquer les autres rôles
    if request.user.role != "TABLE":
        return HttpResponseForbidden("Accès interdit")

    # Vérifier que l'utilisateur TABLE a une table liée
    table = TableRestaurant.objects.filter(utilisateur=request.user).first()
    if not table:
        messages.error(request, "Votre compte n'est lié à aucune table. Contactez l'admin.")
        return redirect("/logout/")

    plats = Plat.objects.all()

    # Ajouter au panier
    if request.method == "POST":
        plat_id = request.POST.get("plat_id")
        if plat_id:
            plat = get_object_or_404(Plat, id=plat_id)

            panier, _ = Panier.objects.get_or_create(table=table)

            item = PanierItem.objects.filter(panier=panier, plat=plat).first()
            if item:
                item.quantite += 1
                item.save()
            else:
                PanierItem.objects.create(panier=panier, plat=plat, quantite=1)

            messages.success(request, f"{plat.nom} ajouté au panier ✅")
            return redirect("/")  # évite le double POST si refresh

    return render(request, "plats.html", {"plats": plats})


# ==========================
# PANIER (TABLE)
# ==========================
@login_required
def panier(request):
    if request.user.role != "TABLE":
        return HttpResponseForbidden("Accès interdit")

    table = TableRestaurant.objects.filter(utilisateur=request.user).first()
    if not table:
        messages.error(request, "Votre compte n'est lié à aucune table. Contactez l'admin.")
        return redirect("/")

    panier, _ = Panier.objects.get_or_create(table=table)

    # Valider commande
    if request.method == "POST":
        if panier.items.count() == 0:
            messages.error(request, "Panier vide.")
            return redirect("/panier/")

        commande = Commande.objects.create(
            table=table,
            total=panier.total()
        )

        # Copier items du panier -> commande
        for item in panier.items.all():
            CommandeItem.objects.create(
                commande=commande,
                plat=item.plat,
                quantite=item.quantite
            )

        # Vider panier
        panier.items.all().delete()

        messages.success(request, "Commande envoyée ✅")
        return redirect("/")

    return render(request, "panier.html", {"panier": panier})


# ==========================
# DASHBOARD SERVEUR
# ==========================
@login_required
def serveur_dashboard(request):
    if request.user.role != "SERVEUR":
        return HttpResponseForbidden("Accès interdit")

    commandes = Commande.objects.filter(etat="EN_ATTENTE").order_by("-id")
    return render(request, "serveur.html", {"commandes": commandes})


@login_required
def prendre_commande(request, commande_id):
    if request.user.role != "SERVEUR":
        return HttpResponseForbidden("Accès interdit")

    commande = get_object_or_404(Commande, id=commande_id)
    commande.etat = "EN_PREPARATION"
    commande.save()

    messages.success(request, f"Commande #{commande.id} prise ✅")
    return redirect("/serveur/")


# ==========================
# DASHBOARD CUISINE
# ==========================
@login_required
def cuisine_dashboard(request):
    if request.user.role != "CUISINE":
        return HttpResponseForbidden("Accès interdit")

    commandes = Commande.objects.filter(etat="EN_PREPARATION").order_by("-id")
    return render(request, "cuisine.html", {"commandes": commandes})


@login_required
def commande_prete(request, commande_id):
    if request.user.role != "CUISINE":
        return HttpResponseForbidden("Accès interdit")

    commande = get_object_or_404(Commande, id=commande_id)
    commande.etat = "PRETE"
    commande.save()

    messages.success(request, f"Commande #{commande.id} prête 🍳")
    return redirect("/cuisine/")




@staff_member_required
def admin_dashboard(request):
    commandes = Commande.objects.all().order_by("-id")
    return render(request, "admin_dashboard.html", {"commandes": commandes})