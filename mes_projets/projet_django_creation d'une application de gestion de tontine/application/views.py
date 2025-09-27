from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm, LoginForm
from .models import Profile


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Vérifie si le profil existe déjà avant de le créer
            if not hasattr(user, 'profile'):
                Profile.objects.create(
                    user=user,
                    prenom=form.cleaned_data['prenom'],
                    age=form.cleaned_data['age'],
                    sexe=form.cleaned_data['sexe']
                )
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Vérifier si c'est un admin tontine
                if hasattr(user, 'profile') and user.profile.is_tontine_admin:
                    return redirect('application:admin_tontine_dashboard')
                else:
                    return redirect('application:acceuil')
            else:
                messages.error(request, 'Identifiants incorrects.')
    else:
        form = LoginForm()
    return render(request, 'connexion.html', {'form': form})



@login_required
def acceuil(request):
    # Statistiques des cotisations
    cotisations = Cotisation.objects.filter(membre=request.user)
    total_cotisations = cotisations.aggregate(total=Sum('montant'))['total'] or 0
    
    # Statistiques des prêts
    prets = Pret.objects.filter(emprunteur=request.user)
    total_prets = prets.aggregate(total=Sum('montant'))['total'] or 0
    
    # Statistiques des dons
    dons = Don.objects.filter(donateur=request.user)
    total_dons = dons.aggregate(total=Sum('montant'))['total'] or 0
    
    # Statistiques des remboursements
    remboursements = Remboursement.objects.filter(membre=request.user)
    total_remboursements = remboursements.aggregate(total=Sum('montant'))['total'] or 0

    context = {
        'total_cotisations': total_cotisations,
        'total_prets': total_prets,
        'total_dons': total_dons,
        'total_remboursements': total_remboursements,
    }
    
    return render(request, 'acceuil.html', context)

def deconnexion(request):
    logout(request)
    return redirect('application:connexion')


 
 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cotisation, Remboursement
from .form import CotisationForm, RemboursementForm,RemboursementPretForm


@login_required
def creer_cotisation(request, montant=None):
    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            cotisation = form.save(commit=False)
            cotisation.membre = request.user
            cotisation.statut = 'ATT'  # Statut initial "En attente"
            cotisation.save()
            return redirect('application:paiement_cotisation', cotisation_id=cotisation.id)
    else:
        initial = {}
        if montant:
            initial = {
                'montant': montant,
                'nom_tontine': f"Tontine {montant}FCFA",
                'frequence': 'H'  # Valeur par défaut Hebdomadaire
            }
        form = CotisationForm(initial=initial)

    # Récupérer les membres ayant déjà cotisé le montant spécifié
    membres_cotisant = None
    if montant in [2000, 10000]:  # Ajout de 2000 ici
        membres_cotisant = User.objects.filter(
            cotisation__montant=montant
        ).distinct().exclude(id=request.user.id)  # Exclure l'utilisateur actuel

    return render(request, 'cotisations/creer.html', {
        'form': form,
        'membres_cotisant': membres_cotisant,
        'montant_tontine': montant
    })
    
@login_required
def paiement_cotisation(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id, membre=request.user)
    
    if request.method == 'POST':
        methode = request.POST.get('methode')
        numero = request.POST.get('numero', '')
        
        cotisation.methode_paiement = methode
        cotisation.date_paiement = timezone.now()
        cotisation.est_active = True
        cotisation.save()
        
        messages.success(request, 'Paiement effectué avec succès!')
        return redirect('application:liste_cotisations')
    
    return render(request, 'cotisations/paiement.html', {
        'cotisation': cotisation
    })

@login_required
def liste_cotisations(request):
    cotisations = Cotisation.objects.filter(membre=request.user)
    return render(request, 'cotisations/liste.html', {'cotisations': cotisations})

# Remboursements
@login_required
def demander_remboursement(request):
    if request.method == 'POST':
        form = RemboursementForm(request.POST, user=request.user)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.membre = request.user
            remboursement.save()
            return redirect('application:liste_remboursements')
    else:
        form = RemboursementForm(user=request.user)
    return render(request, 'remboursements/demander.html', {'form': form})

@login_required
def liste_remboursements(request):
    remboursements = Remboursement.objects.filter(membre=request.user)
    return render(request, 'remboursements/liste.html', {'remboursements': remboursements})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Don
from .form import DonForm
from decimal import Decimal

@login_required
def faire_don(request, type_don):
    type_map = {
        'solidarite': 'Dons de solidarite',
        'projet': 'Dons pour les projets communs',
        'ponctuel': 'Dons financier unique',
        'nature': 'Dons en nature'
    }

    if type_don not in type_map:
        return redirect('application:acceuil')

    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            if not don.anonyme:
                don.donateur = request.user
            don.type_don = type_map[type_don]
            don.save()
            return redirect('application:confirmation_don', type_don=type_don, don_id=don.id)
    else:
        form = DonForm()

    context = {
        'form': form,
        'type_don': type_don,
        'page_title': {
            'solidarite': 'Cadeau de solidarité',
            'projet': 'Don pour un projet commun',
            'ponctuel': 'Don financier ponctuel',
            'nature': 'Don en nature'
        }.get(type_don, 'Faire un don'),
        'description': {
            'solidarite': "Un soutien entre membres de la tontine.",
            'projet': "Aidez à financer un projet collectif.",
            'ponctuel': "Soutenez un membre dans un moment difficile.",
            'nature': "Faites un don en biens ou services."
        }.get(type_don, ''),
    }

    return render(request, 'dons/faire.html', context)

@login_required
def liste_dons(request):
    dons = Don.objects.filter(donateur=request.user)
    total = sum(don.montant if don.montant is not None else Decimal(0) for don in dons)
    return render(request, 'dons/liste.html', {
        'dons': dons,
        'total': total,
        'STATUT_CHOICES': Don.STATUT_CHOICES
    })



from django.shortcuts import get_object_or_404

@login_required
def confirmation_don(request, type_don, don_id):
    # Get the donation by ID only, regardless of donateur
    don = get_object_or_404(Don, id=don_id)

    # Optional: Make sure the logged-in user is either the donateur OR the donation is anonymous
    if don.donateur and don.donateur != request.user:
        return redirect('application:acceuil')  # Prevent unauthorized access

    context = {
        'don': don,
        'type_don': don.type_don,
        'confirmation_message': {
            'solidarite': "Merci pour votre cadeau de solidarité !",
            'projet': "Merci pour votre contribution au projet commun !",
            'ponctuel': "Merci pour votre don ponctuel !",
            'nature': "Merci pour votre don en nature !"
        }.get(don.type_don, "Merci pour votre don !")
    }
    return render(request, 'dons/confirmation.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pret
from .form import PretForm


@login_required
def demander_pret(request):
    if request.method == 'POST':
        form = PretForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            pret = form.save(commit=False)
            pret.emprunteur = request.user
            pret.save()
            return redirect('application:apercu_remboursement', pret_id=pret.id)
    else:
        form = PretForm(user=request.user)
    
    return render(request, 'prets/demander.html', {'form': form})

@login_required
def liste_prets(request):
    prets = Pret.objects.filter(emprunteur=request.user)
    return render(request, 'prets/liste.html', {'prets': prets})

@login_required
def confirmation_pret(request, pret_id):
    pret = get_object_or_404(Pret, id=pret_id, emprunteur=request.user)
    return render(request, 'prets/confirmation.html', {'pret': pret})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .form import MembreCreationForm, MembreUpdateForm
from .models import Membre

@login_required
def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'membres/liste.html', {'membres': membres})

@login_required
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Membre.objects.create(user=user, age=form.cleaned_data['age'])
            return redirect('application:liste_membres')
    else:
        form = MembreCreationForm()
    return render(request, 'membres/ajouter.html', {'form': form})


@login_required
def modifier_membre(request, user_id):
    user = get_object_or_404(User, id=user_id)
    membre = get_object_or_404(Membre, user=user)  # Récupère l'objet Membre associé
    
    if request.method == 'POST':
        form = MembreUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Sauvegarde les données du User
            user = form.save()
            
            # Met à jour l'âge dans le modèle Membre
            new_age = request.POST.get('age')
            if new_age:
                membre.age = new_age
                membre.save()  # N'oubliez pas de sauvegarder le modèle Membre
            
            return redirect('application:liste_membres')
    else:
        form = MembreUpdateForm(instance=user)
    
    return render(request, 'membres/modifier.html', {
        'form': form,
        'membre': membre  # Passez l'objet membre au template
    })
@login_required
def supprimer_membre(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('application:liste_membres')
    return render(request, 'membres/supprimer.html', {'membre': user})



from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import datetime, date, timedelta


import json
@login_required
def tableau_de_bord(request):
    # Statistiques des cotisations
    cotisations = Cotisation.objects.filter(membre=request.user)
    total_cotisations = cotisations.aggregate(total=Sum('montant'))['total'] or 0
    cotisations_actives = cotisations.filter(est_active=True).count()
    cotisations_payees = cotisations.filter(date_paiement__isnull=False).count()
    pourcentage_cotisations = (cotisations_payees / cotisations.count() * 100) if cotisations.count() > 0 else 0
    
    # Statistiques des prêts
    prets = Pret.objects.filter(emprunteur=request.user)
    total_prets = prets.aggregate(total=Sum('montant'))['total'] or 0
    prets_en_cours = prets.exclude(statut__in=['REM', 'REF']).count()
    prets_rembourses = prets.filter(statut='REM').count()
    pourcentage_prets = (prets_rembourses / prets.count() * 100) if prets.count() > 0 else 0
    
    # Statistiques des dons
    dons = Don.objects.filter(donateur=request.user)
    total_dons = dons.aggregate(total=Sum('montant'))['total'] or 0
    dons_count = dons.count()
    
    # Statistiques des remboursements
    remboursements = Remboursement.objects.filter(membre=request.user)
    total_remboursements = remboursements.aggregate(total=Sum('montant'))['total'] or 0
    remboursements_tontine = remboursements.filter(type_remboursement='COT').count()
    remboursements_pret = remboursements.filter(type_remboursement='PRET').count()
    
    # Activités récentes (30 derniers jours)
    date_limite = timezone.now() - timedelta(days=30)
    activites_recentes = []
    
    # Conversion de date_limite en datetime.date si nécessaire
    if isinstance(date_limite, datetime):
        date_limite = date_limite.date()
    
    # Cotisations récentes
    for cotisation in cotisations.filter(date_debut__gte=date_limite):
        activites_recentes.append({
            'type': 'Cotisation',
            'montant': cotisation.montant,
            'date': cotisation.date_debut.date() if hasattr(cotisation.date_debut, 'date') else cotisation.date_debut,
            'statut': cotisation.get_statut_display(),
            'details': f"{cotisation.get_frequence_display()}"
        })
    
    # Prêts récents
    for pret in prets.filter(date_demande__gte=date_limite):
        activites_recentes.append({
            'type': 'Prêt',
            'montant': pret.montant,
            'date': pret.date_demande.date() if hasattr(pret.date_demande, 'date') else pret.date_demande,
            'statut': pret.get_statut_display(),
            'details': pret.motif[:50] + '...' if pret.motif else ''
        })
    
    # Dons récents
    for don in dons.filter(date__gte=date_limite):
        activites_recentes.append({
            'type': 'Don',
            'montant': don.montant if don.montant else 0,
            'date': don.date.date() if hasattr(don.date, 'date') else don.date,
            'statut': don.get_statut_display(),
            'details': don.type_don
        })
    
    # Remboursements récents
    for remboursement in remboursements.filter(date_demande__gte=date_limite):
        activites_recentes.append({
            'type': 'Remboursement',
            'montant': remboursement.montant,
            'date': remboursement.date_demande.date() if hasattr(remboursement.date_demande, 'date') else remboursement.date_demande,
            'statut': remboursement.get_statut_display(),
            'details': remboursement.get_type_remboursement_display()
        })
    
    # Tri par date (en s'assurant que toutes les dates sont des objets date)
    activites_recentes.sort(key=lambda x: x['date'] if isinstance(x['date'], date) else x['date'].date(), reverse=True)
    
    # Données pour les graphiques
    mois = []
    montants_prets = []
    
    # Générer les données des 6 derniers mois
    for i in range(5, -1, -1):
        date_mois = timezone.now() - timedelta(days=30*i)
        mois.append(date_mois.strftime("%b %Y"))
        
        total_mois = prets.filter(
            date_demande__month=date_mois.month,
            date_demande__year=date_mois.year
        ).aggregate(total=Sum('montant'))['total'] or 0
        montants_prets.append(float(total_mois))
    
    context = {
        'total_cotisations': total_cotisations,
        'cotisations_actives': cotisations_actives,
        'cotisations_payees': cotisations_payees,
        'pourcentage_cotisations': pourcentage_cotisations,
        'total_prets': total_prets,
        'prets_en_cours': prets_en_cours,
        'prets_rembourses': prets_rembourses,
        'pourcentage_prets': pourcentage_prets,
        'total_dons': total_dons,
        'dons_count': dons_count,
        'total_remboursements': total_remboursements,
        'remboursements_tontine': remboursements_tontine,
        'remboursements_pret': remboursements_pret,
        'activites_recentes': activites_recentes[:10],
        'mois': json.dumps(mois),  # Convertir en JSON pour le JavaScript
        'montants_prets': json.dumps(montants_prets)  # Convertir en JSON pour le JavaScript
    }
    
    return render(request, 'tableau_de_bord.html', context)


from django.contrib.auth.decorators import user_passes_test

def is_tontine_admin(user):
    return hasattr(user, 'profile') and user.profile.is_tontine_admin



@login_required
@user_passes_test(is_tontine_admin)
def admin_tontine_dashboard(request):
    # Statistiques générales
    total_membres = User.objects.count()
    total_cotisations = Cotisation.objects.count()
    total_prets = Pret.objects.count()
    total_dons = Don.objects.count()
    total_remboursements = Remboursement.objects.count()
    
    # Données pour le diagramme des âges
    age_distribution = Profile.objects.exclude(age__isnull=True).values('age').annotate(count=Count('age')).order_by('age')
    
    # Créer des groupes d'âge
    age_groups = {
        '18-25': 0,
        '26-35': 0,
        '36-45': 0,
        '46+': 0,
        'Non spécifié': Profile.objects.filter(age__isnull=True).count()
    }
    
    for age in age_distribution:
        if age['age'] is not None:  # Vérification supplémentaire
            if 18 <= age['age'] <= 25:
                age_groups['18-25'] += age['count']
            elif 26 <= age['age'] <= 35:
                age_groups['26-35'] += age['count']
            elif 36 <= age['age'] <= 45:
                age_groups['36-45'] += age['count']
            else:
                age_groups['46+'] += age['count']
    
    # Données pour le diagramme des types de tontines
    tontine_types = Cotisation.objects.values('montant').annotate(count=Count('montant'))
    tontine_data = {
        '10000': 0,
        '2000': 0,
        'presence': 0
    }
    
    for tontine in tontine_types:
        if tontine['montant'] == 10000:
            tontine_data['10000'] = tontine['count']
        elif tontine['montant'] == 2000:
            tontine_data['2000'] = tontine['count']
        else:
            tontine_data['presence'] += tontine['count']
    
    # Données pour le diagramme des types de dons
    don_types = Don.objects.values('type_don').annotate(count=Count('type_don'))
    don_data = {
        'solidarite': 0,
        'projet': 0,
        'ponctuel': 0,
        'nature': 0
    }
    
    for don in don_types:
        if 'solidarite' in don['type_don'].lower():
            don_data['solidarite'] = don['count']
        elif 'projet' in don['type_don'].lower():
            don_data['projet'] = don['count']
        elif 'ponctuel' in don['type_don'].lower():
            don_data['ponctuel'] = don['count']
        elif 'nature' in don['type_don'].lower():
            don_data['nature'] = don['count']
    
    context = {
        'total_membres': total_membres,
        'total_cotisations': total_cotisations,
        'total_prets': total_prets,
        'total_dons': total_dons,
        'total_remboursements': total_remboursements,
        'age_data': list(age_groups.values()),
        'age_labels': json.dumps(list(age_groups.keys())),  # Convertir en JSON pour JavaScript
        'tontine_data': list(tontine_data.values()),
        'don_data': list(don_data.values()),
    }
    return render(request, 'admin_tontine/dashboard.html', context)


@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_membres(request):
    membres = User.objects.all().order_by('date_joined')
    return render(request, 'admin_tontine/liste_membres.html', {'membres': membres})

@login_required
@user_passes_test(is_tontine_admin)
def admin_supprimer_membre(request, user_id):
    membre = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        membre.delete()
        messages.success(request, 'Membre supprimé avec succès.')
        return redirect('application:admin_liste_membres')
    return render(request, 'admin_tontine/supprimer_membre.html', {'membre': membre})



@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_cotisations(request):
    cotisations = Cotisation.objects.all().select_related('membre').order_by('-date_debut')
    return render(request, 'admin_tontine/liste_cotisations.html', {'cotisations': cotisations})

@login_required
@user_passes_test(is_tontine_admin)
def admin_detail_cotisation(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    membres = User.objects.filter(cotisation__id=cotisation_id).distinct()
    return render(request, 'admin_tontine/detail_cotisation.html', {
        'cotisation': cotisation,
        'membres': membres
    })

@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_prets(request):
    prets = Pret.objects.all().select_related('emprunteur')
    return render(request, 'admin_tontine/liste_prets.html', {'prets': prets})

@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_pret(request, pret_id):
    pret = get_object_or_404(Pret, id=pret_id)
    if request.method == 'POST':
        pret.statut = 'ACC'
        pret.date_approbation = timezone.now()
        pret.save()
        messages.success(request, 'Prêt approuvé avec succès.')
        return redirect('application:admin_liste_prets')
    return render(request, 'admin_tontine/valider_pret.html', {'pret': pret})



@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_dons(request):
    dons = Don.objects.all().select_related('donateur')
    return render(request, 'admin_tontine/liste_dons.html', {
        'dons': dons,
        'STATUT_CHOICES': Don.STATUT_CHOICES
    })

@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_don(request, don_id):
    don = get_object_or_404(Don, id=don_id)
    # Ici vous pourriez ajouter une logique de validation si nécessaire
    messages.success(request, 'Don validé avec succès.')
    return redirect('application:admin_liste_dons')

@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_remboursements(request):
    remboursements = Remboursement.objects.all().select_related('membre', 'cotisation')
    return render(request, 'admin_tontine/liste_remboursements.html', {'remboursements': remboursements})

@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_remboursement(request, remboursement_id):
    remboursement = get_object_or_404(Remboursement, id=remboursement_id)
    if request.method == 'POST':
        remboursement.statut = 'A'
        remboursement.save()
        messages.success(request, 'Remboursement approuvé avec succès.')
        return redirect('application:admin_liste_remboursements')
    return render(request, 'admin_tontine/valider_remboursement.html', {'remboursement': remboursement})


@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_don(request, don_id):
    don = get_object_or_404(Don, id=don_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            don.statut = 'VAL'
            messages.success(request, 'Don validé avec succès.')
        elif action == 'refuser':
            don.statut = 'REF'
            messages.warning(request, 'Don refusé.')
        don.save()
        return redirect('application:admin_liste_dons')
    
    return render(request, 'admin_tontine/valider_don.html', {'don': don})



@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_cotisation(request, cotisation_id):
    cotisation = get_object_or_404(Cotisation, id=cotisation_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        commentaire = request.POST.get('commentaire', '')
        
        if action == 'valider':
            cotisation.statut = 'VAL'
            messages.success(request, f'La cotisation {cotisation.nom_tontine} a été validée avec succès.')
        elif action == 'refuser':
            cotisation.statut = 'REF'
            messages.warning(request, f'La cotisation {cotisation.nom_tontine} a été refusée.')
        
        if commentaire:
            # Vous pouvez stocker le commentaire dans un champ supplémentaire si nécessaire
            pass
            
        cotisation.save()
        return redirect('application:admin_liste_cotisations')
    
    return render(request, 'admin_tontine/valider_cotisation.html', {
        'cotisation': cotisation
    })

# Dans views.py
@login_required
def apercu_remboursement(request, pret_id):
    pret = get_object_or_404(Pret, id=pret_id, emprunteur=request.user)
    
    if request.method == 'POST':
        pret.save()  # Cela va calculer le montant à rembourser
        return redirect('application:confirmation_pret', pret_id=pret.id)
    
    return render(request, 'prets/apercu_remboursement.html', {
        'pret': pret,
        'interet': pret.montant_a_rembourser - pret.montant if pret.montant_a_rembourser else 0
    })
    
    

# Dans views.py, ajoutez ces nouvelles vues
@login_required
def demander_remboursement_pret(request):
    if request.method == 'POST':
        form = RemboursementPretForm(request.POST, user=request.user)
        if form.is_valid():
            remboursement = form.save(commit=False)
            remboursement.membre = request.user
            remboursement.type_remboursement = 'PRET'
            remboursement.save()
            return redirect('application:paiement_remboursement_pret', remboursement_id=remboursement.id)
    else:
        form = RemboursementPretForm(user=request.user)
    
    return render(request, 'remboursements/demander_pret.html', {
        'form': form,
        'page_title': 'Remboursement de prêt'
    })


@login_required
def paiement_remboursement_pret(request, remboursement_id):
    remboursement = get_object_or_404(
        Remboursement, 
        id=remboursement_id, 
        membre=request.user, 
        type_remboursement='PRET'
    )
    
    if request.method == 'POST':
        methode = request.POST.get('methode')
        numero = request.POST.get('numero', '')
        
        # Mettre à jour le montant déjà remboursé
        pret = remboursement.pret
        pret.montant_deja_rembourse += remboursement.montant
        
        # Si le prêt est entièrement remboursé, changer son statut
        if pret.reste_a_rembourser <= 0:
            pret.statut = 'REM'
        
        pret.save()
        
        messages.success(request, 'Paiement effectué avec succès!')
        return redirect('application:liste_remboursements_pret')
    
    return render(request, 'remboursements/paiement_pret.html', {
        'remboursement': remboursement,
        'pret': remboursement.pret
    })

@login_required
def liste_remboursements_pret(request):
    remboursements = Remboursement.objects.filter(
        membre=request.user,
        type_remboursement='PRET'
    ).order_by('-date_demande')
    
    return render(request, 'remboursements/liste_pret.html', {
        'remboursements': remboursements,
        'STATUTS': Remboursement.STATUTS
    })
    
    
    
# Dans views.py
@login_required
@user_passes_test(is_tontine_admin)
def admin_liste_remboursements_pret(request):
    remboursements = Remboursement.objects.filter(
        type_remboursement='PRET'
    ).select_related('membre', 'pret').order_by('-date_demande')
    
    return render(request, 'admin_tontine/liste_remboursements_pret.html', {
        'remboursements': remboursements
    })

@login_required
@user_passes_test(is_tontine_admin)
def admin_detail_remboursement_pret(request, remboursement_id):
    remboursement = get_object_or_404(
        Remboursement, 
        id=remboursement_id, 
        type_remboursement='PRET'
    )
    return render(request, 'admin_tontine/detail_remboursement_pret.html', {
        'remboursement': remboursement
    })

@login_required
@user_passes_test(is_tontine_admin)
def admin_valider_remboursement_pret(request, remboursement_id):
    remboursement = get_object_or_404(
        Remboursement, 
        id=remboursement_id, 
        type_remboursement='PRET'
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        commentaire = request.POST.get('commentaire', '')
        
        if action == 'valider':
            remboursement.statut = 'A'
            remboursement.date_validation = timezone.now().date()
            messages.success(request, 'Remboursement validé avec succès.')
        elif action == 'refuser':
            remboursement.statut = 'R'
            messages.warning(request, 'Remboursement refusé.')
        
        remboursement.commentaire = commentaire
        remboursement.save()
        
        return redirect('application:admin_liste_remboursements_pret')
    
    return render(request, 'admin_tontine/valider_remboursement_pret.html', {
        'remboursement': remboursement
    })
    
    
    
from django.http import JsonResponse

@login_required
def pret_details_api(request, pret_id):
    pret = get_object_or_404(Pret, id=pret_id, emprunteur=request.user)
    return JsonResponse({
        'montant': float(pret.montant),
        'montant_a_rembourser': float(pret.montant_a_rembourser),
        'montant_deja_rembourse': float(pret.montant_deja_rembourse),
        'reste_a_rembourser': float(pret.reste_a_rembourser),
    })
    
    