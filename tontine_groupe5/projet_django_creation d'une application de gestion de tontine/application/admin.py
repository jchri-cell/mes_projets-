from django.contrib import admin
from .models import Don
from application.models import Cotisation, Utilisateur,Profile, Remboursement,Don,Pret,Membre

class DonAdmin(admin.ModelAdmin):
    list_display = ('type_don', 'montant', 'nature', 'methode', 'anonyme', 'date')
    list_filter = ('type_don', 'methode', 'anonyme')

admin.site.register(Don, DonAdmin)
admin.site.register(Cotisation)
admin.site.register(Utilisateur)
admin.site.register(Profile)
admin.site.register(Remboursement)
admin.site.register(Pret)
admin.site.register(Membre)