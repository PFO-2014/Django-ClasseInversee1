# -*- coding: utf-8 -*-

from django.contrib import admin
from MonEtablissement.models import MesClasse, MesSequence, MesSeance,\
    MesActivite, Eleve
from django.contrib.admin.helpers import Fieldset




class MesSequencesInline(admin.TabularInline):
    model = MesSequence
    extra = 1
    
class MesActiviteInline(admin.TabularInline):
    model = MesActivite
    extra = 1



class MesClassesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Mon établissement', {'fields': ['nom_etablissement_text']}),
        ('Niveau', {'fields': ['niveau']}),
        ('Année Scolaire', {'fields': ['annee_cours_dateint']}),
    ]
    inlines = [MesSequencesInline]

class MesSeanceAdmin(admin.ModelAdmin):
    inlines = [MesActiviteInline]
    
class MesSequenceAdmin(admin.ModelAdmin):
    list_display = ('short_description_sequence', 'niveau_indicatif')
    list_filter = ('short_description_sequence', 'niveau_indicatif')
    
    Fieldset = [
                ('Séquence', {'fields': ['short_description_sequence']}),
                ('Niveau', {'fields': ['niveau_indicatif']})
                ]


# Register your models here.
admin.site.register(MesClasse, MesClassesAdmin)
admin.site.register(MesSequence, MesSequenceAdmin)
admin.site.register(MesSeance, MesSeanceAdmin)
admin.site.register(MesActivite)
admin.site.register(Eleve)

