from django.urls import path, include
from django import views   
from .views import *
from django.urls import path


from django.contrib import admin
from django.urls import path
from application import views



from django.urls import path
from . import views


app_name = 'application'

urlpatterns = [
    

    path('cotisations/creer/', views.creer_cotisation, name='creer_cotisation'),
    path('cotisations/creer/<int:montant>/', views.creer_cotisation, name='creer_cotisation_montant'),
    path('cotisations/<int:cotisation_id>/paiement/', views.paiement_cotisation, name='paiement_cotisation'),
    path('cotisations/', views.liste_cotisations, name='liste_cotisations'),
    path('admin-tontine/cotisations/<int:cotisation_id>/valider/', 
     views.admin_valider_cotisation, 
     name='admin_valider_cotisation'),
    
    # URLs admin pour validation
    path('admin-tontine/cotisations/<int:cotisation_id>/valider/', views.admin_valider_cotisation, name='admin_valider_cotisation'),
    path('remboursements/demander/', views.demander_remboursement, name='demander_remboursement'),
    path('remboursements/demander/', views.demander_remboursement, name='demander_remboursement'),
    path('remboursements/', views.liste_remboursements, name='liste_remboursements'),
    path('donner/<str:type_don>/', views.faire_don, name='faire_don'),
    path('confirmation/<str:type_don>/<int:don_id>/', views.confirmation_don, name='confirmation_don'),
    path('liste/', views.liste_dons, name='liste_dons'),path('prets/demander/', views.demander_pret, name='demander_pret'),
    path('prets/', views.liste_prets, name='liste_prets'),
    path('prets/confirmation/<int:pret_id>/', views.confirmation_pret, name='confirmation_pret'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('membres/ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('membres/<int:user_id>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('membres/<int:user_id>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('admin-tontine/', views.admin_tontine_dashboard, name='admin_tontine_dashboard'),
    path('admin-tontine/membres/', views.admin_liste_membres, name='admin_liste_membres'),
    path('admin-tontine/membres/<int:user_id>/supprimer/', views.admin_supprimer_membre, name='admin_supprimer_membre'),
    path('admin-tontine/cotisations/', views.admin_liste_cotisations, name='admin_liste_cotisations'),
    path('admin-tontine/cotisations/<int:cotisation_id>/', views.admin_detail_cotisation, name='admin_detail_cotisation'),
    path('admin-tontine/prets/', views.admin_liste_prets, name='admin_liste_prets'),
    path('admin-tontine/prets/<int:pret_id>/valider/', views.admin_valider_pret, name='admin_valider_pret'),
    path('admin-tontine/dons/', views.admin_liste_dons, name='admin_liste_dons'),
    path('admin-tontine/dons/<int:don_id>/valider/', views.admin_valider_don, name='admin_valider_don'),
    path('admin-tontine/remboursements/', views.admin_liste_remboursements, name='admin_liste_remboursements'),
    path('admin-tontine/remboursements/<int:remboursement_id>/valider/', views.admin_valider_remboursement, name='admin_valider_remboursement'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('admin-tontine/dons/<int:don_id>/valider/', views.admin_valider_don, name='admin_valider_don'),
    path('prets/apercu/<int:pret_id>/', views.apercu_remboursement, name='apercu_remboursement'),
    # Dans urls.py, ajoutez ces nouvelles URLs
    path('remboursements-pret/demander/', views.demander_remboursement_pret, name='demander_remboursement_pret'),
    path('remboursements-pret/<int:remboursement_id>/paiement/', views.paiement_remboursement_pret, name='paiement_remboursement_pret'),
    path('remboursements-pret/', views.liste_remboursements_pret, name='liste_remboursements_pret'),
    path('admin-tontine/remboursements-pret/', 
         views.admin_liste_remboursements_pret, 
         name='admin_liste_remboursements_pret'),
    path('admin-tontine/remboursements-pret/<int:remboursement_id>/', 
         views.admin_detail_remboursement_pret, 
         name='admin_detail_remboursement_pret'),
    path('admin-tontine/remboursements-pret/<int:remboursement_id>/valider/', 
         views.admin_valider_remboursement_pret, 
         name='admin_valider_remboursement_pret'),
    path('api/pret-details/<int:pret_id>/', views.pret_details_api, name='pret_details_api'),

       
]

