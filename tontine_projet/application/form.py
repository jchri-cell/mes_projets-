from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import Profile
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[validate_email]
    )
    nom = forms.CharField(label="Nom", required=True)
    prenom = forms.CharField(label="Prénom", required=True)
    age = forms.IntegerField(label="Âge", required=False)
    sexe = forms.ChoiceField(
        label="Sexe",
        choices=[('', '---------'), ('M', 'Masculin'), ('F', 'Féminin')],
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'nom', 'prenom', 'password1', 'password2')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['prenom']  # ou nom selon votre logique
        user.last_name = self.cleaned_data['nom']      # ou prenom selon votre logique
        if commit:
            user.save()
        return user


from django.contrib.auth import authenticate
class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        
        return cleaned_data
        

from django import forms
from .models import Cotisation, Remboursement


class CotisationForm(forms.ModelForm):
    class Meta:
        model = Cotisation
        fields = ['nom_tontine', 'montant', 'frequence']
        widgets = {
            'montant': forms.NumberInput(attrs={
                'min': 0, 
                'step': 1000,
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'nom_tontine': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control'
            }),
            'frequence': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        montant_tontine = kwargs.pop('montant_tontine', None)
        super().__init__(*args, **kwargs)
        if montant_tontine:
            self.initial['montant'] = montant_tontine
            self.initial['nom_tontine'] = f"Tontine {montant_tontine}FCFA"

class RemboursementForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ['cotisation', 'montant']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cotisation'].queryset = Cotisation.objects.filter(
                membre=user, 
                est_active=True
            )


            

from django import forms
from .models import Don

class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        exclude = ['donateur','type_don']
        fields = ['montant', 'type_don', 'methode', 'message', 'anonyme', 'nature']
        widgets = {
            'nature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type de bien ou service'}),
            'message': forms.Textarea(attrs={'rows': 3}),
            'montant': forms.NumberInput(attrs={'min': 1000}),
        }
        labels = {
            'anonyme': "Faire un don anonyme"
        }
    def clean(self):
        cleaned_data = super().clean()
        type_don = cleaned_data.get("type_don")
        montant = cleaned_data.get("montant")
        nature = cleaned_data.get("nature")

        if type_don == "nature" and not nature:
            self.add_error('nature', "Ce champ est requis pour un don en nature.")
        elif type_don != "nature" and not montant:
            self.add_error('montant', "Veuillez saisir un montant.")
        return cleaned_data
    widgets = {
            'nature': forms.TextInput(attrs={
                'placeholder': 'Ex: Vêtements pour enfants, sacs de riz...',
                'class': 'form-control'
            }),
        }

        
from django import forms
from .models import Pret
from django.contrib.auth import get_user_model

User = get_user_model()



# Dans form.py
class PretForm(forms.ModelForm):
    class Meta:
        model = Pret
        fields = ['cotisation', 'montant', 'motif', 'avaliseur', 'infos_avaliseur', 'periode_remboursement', 'fichier_avaliseur']
        widgets = {
            'motif': forms.Textarea(attrs={'rows': 3, 'placeholder': "Détaillez l'utilisation du prêt"}),
            'montant': forms.NumberInput(attrs={'min': 5000, 'step': 1000, 'max': 30000}),  # Ajout de max=30000
            'infos_avaliseur': forms.Textarea(attrs={'rows': 3, 'placeholder': "Informations complètes sur l'avaliseur"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['cotisation'].queryset = Cotisation.objects.filter(
                membre=self.user,
                est_active=True,
                statut='VAL'
            )
            self.fields['avaliseur'].queryset = User.objects.exclude(id=self.user.id)

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant > 30000:  # Limite de 30 000 FCFA
            raise forms.ValidationError("Le montant du prêt ne peut pas dépasser 30 000 FCFA")
        return montant


            
            
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Membre

class MembreCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    email = forms.EmailField(required=True)
    age = forms.IntegerField(label="Âge", min_value=18)
    
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class MembreUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        
        
# Dans form.py, ajoutez cette classe
class RemboursementPretForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ['pret', 'montant']
        widgets = {
            'montant': forms.NumberInput(attrs={
                'min': 0,
                'step': 1000,
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pret'].queryset = Pret.objects.filter(
                emprunteur=user,
                statut='ACC'
            ).exclude(statut='REM')
    
    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        pret = self.cleaned_data.get('pret')
        
        if pret and montant:
            if montant > pret.reste_a_rembourser:
                raise forms.ValidationError(
                    f"Le montant ne peut pas dépasser {pret.reste_a_rembourser} FCFA (reste à rembourser)"
                )
            if montant <= 0:
                raise forms.ValidationError("Le montant doit être supérieur à 0")
        
        return montant