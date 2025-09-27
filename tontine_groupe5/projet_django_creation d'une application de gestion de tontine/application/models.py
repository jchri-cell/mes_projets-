from django.db import models
from django.db import models
from django.conf import settings  
from django.contrib.auth.models import User

from django.db import models

class Utilisateur(models.Model):
     nom = models.CharField(max_length=50)  
     mot_de_passe = models.CharField(max_length=50)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    sexe = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        null=True,
        blank=True
    )
    is_tontine_admin = models.BooleanField(default=False)  # Ajoutez ce champ

    def __str__(self):
        return f"{self.user.username} - Admin: {self.is_tontine_admin}"
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        # Pour l'admin tontine spécifique
        if instance.username == 'administrateur':
            Profile.objects.update_or_create(
                user=instance,
                defaults={'is_tontine_admin': True}
            )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Cotisation(models.Model):
    FREQUENCES = [
        ('H', 'Hebdomadaire'),
        ('M', 'Mensuelle'),
        ('T', 'Trimestrielle'), 
        ('A', 'Annuelle')
    ]
    
    STATUTS = [
        ('ATT', 'En attente'),
        ('VAL', 'Validé'),
        ('REF', 'Refusé')
    ]
    
    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    nom_tontine = models.CharField(max_length=100, default='')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    frequence = models.CharField(max_length=1, choices=FREQUENCES)
    date_debut = models.DateField(default=timezone.now)
    est_active = models.BooleanField(default=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    methode_paiement = models.CharField(max_length=10, blank=True, null=True)
    statut = models.CharField(max_length=3, choices=STATUTS, default='ATT')

    def __str__(self):
        return f"{self.nom_tontine} - {self.montant}FCFA"

        return f"Remboursement #{self.id}"
    
    

    
    
from django.db import models
from django.contrib.auth.models import User


class Don(models.Model):
    STATUT_CHOICES = [
        ('ATT', 'En attente'),
        ('VAL', 'Validé'),
        ('REF', 'Refusé')
    ]
    
    type_don = models.CharField(max_length=50)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nature = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(blank=True)
    anonyme = models.BooleanField(default=False)
    moyen_paiement = models.CharField(max_length=50, blank=True, null=True)
    donateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    methode = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=3, choices=STATUT_CHOICES, default='ATT')
    
    def __str__(self):
        return f"{self.type_don.capitalize()} - {self.montant or self.nature} ({self.get_statut_display()})"

    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal



# Dans models.py
class Pret(models.Model):
    STATUT_CHOICES = [
        ('DEM', 'Demande en cours'),
        ('ACC', 'Accepté'),
        ('REF', 'Refusé'),
        ('REM', 'Remboursé')
    ]
    
    PERIODE_REMBOURSEMENT = [
        ('1M', '1 mois'),
        ('3M', '3 mois'),
        ('6M', '6 mois'),
        ('1A', '1 an')
    ]

    emprunteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prets')
    cotisation = models.ForeignKey(Cotisation, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    montant_a_rembourser = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    motif = models.TextField()
    date_demande = models.DateTimeField(auto_now_add=True)
    date_approbation = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=3, choices=STATUT_CHOICES, default='DEM')
    avaliseur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prets_avalises')
    periode_remboursement = models.CharField(max_length=2, choices=PERIODE_REMBOURSEMENT, default='1M')
    infos_avaliseur = models.TextField(blank=True, null=True)
    fichier_avaliseur = models.FileField(
        upload_to='avaliseurs/',
        null=True,
        blank=True,
        verbose_name="Fichier d'informations de l'avaliseur (PDF)"
    )
    montant_deja_rembourse = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    @property
    def reste_a_rembourser(self):
        return self.montant_a_rembourser - self.montant_deja_rembourse

    def __str__(self):
        return f"Pret #{self.id} - {self.montant}FCFA"

        
    
    def save(self, *args, **kwargs):
        # Validation du montant avant sauvegarde
        if self.montant > 30000:
            raise ValueError("Le montant du prêt ne peut pas dépasser 30 000 FCFA")
        
        # Calcul du montant à rembourser avec intérêt (5% par exemple)
        if not self.montant_a_rembourser:
            self.montant_a_rembourser = self.montant * Decimal('1.05')
        super().save(*args, **kwargs)
    
    
from django.db import models
from django.contrib.auth.models import User

class Membre(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    telephone = models.CharField(max_length=20, blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"
    

class Remboursement(models.Model):
    STATUTS = [
        ('P', 'En attente'),
        ('A', 'Approuvé'),
        ('R', 'Rejeté')
    ]
    
    TYPE_REMBOURSEMENT = [
        ('COT', 'Cotisation'),
        ('PRET', 'Prêt')
    ]
    
    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    cotisation = models.ForeignKey(Cotisation, on_delete=models.SET_NULL, null=True, blank=True)
    pret = models.ForeignKey(Pret, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_demande = models.DateField(auto_now_add=True)
    date_validation = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=1, choices=STATUTS, default='P')
    type_remboursement = models.CharField(max_length=4, choices=TYPE_REMBOURSEMENT, default='COT')
    commentaire = models.TextField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if self.type_remboursement == 'PRET' and self.pret and self.statut == 'A':
            self.pret.montant_deja_rembourse += self.montant
            if self.pret.reste_a_rembourser <= 0:
                self.pret.statut = 'REM'
            self.pret.save()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"Remboursement #{self.id} - {self.get_type_remboursement_display()}"
    
    