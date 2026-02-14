# 🍽️ Restaurant Django - Système de Commande (TABLE / SERVEUR / CUISINE)

Application web Django qui simule le fonctionnement d’un restaurant :
- une **TABLE** consulte le menu, ajoute des plats au panier et valide une commande
- un **SERVEUR** voit les commandes en attente et les prend en charge
- la **CUISINE** voit les commandes en préparation et les marque comme prêtes
- un **ADMIN** peut gérer les données (plats, utilisateurs, tables, commandes)

## ✅ Fonctionnalités
- Authentification personnalisée par `login` (ex : TABLE, SERVEUR, CUISINE, admin)
- Rôles utilisateur : **TABLE**, **SERVEUR**, **CUISINE**
- Menu des plats avec images (ImageField)
- Panier + validation de commande
- Workflow des commandes :
  - `EN_ATTENTE` → `EN_PREPARATION` → `PRETE`
- Dashboard Serveur + Dashboard Cuisine
- Django Admin + Dashboard Admin (optionnel) pour suivre toutes les commandes
- Interface moderne (Tailwind via CDN)

---

## 🛠️ Installation (local)

### 1) Cloner le projet
```bash
git clone https://github.com/TON-USERNAME/restaurant-django.git
cd restaurant-django
