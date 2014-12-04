# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


"""
CREATION DE LA BASE DE DONNEE
AJOUT DES METHODES DEDIEES
"""



#===============================================================================
# CLASSE -NIVEAU - ETABLISSEMENT - ANNEE SCOLAIRE
#===============================================================================
class MesClasse(models.Model):
    """
    Classe définissant la base de donnée des niveaux
    """
    nom_etablissement_text = models.CharField('mon établissement', max_length=200)
    annee_cours_dateint = models.IntegerField('Année en cours', default=timezone.datetime.today().year, editable=True)
    
    niveau = models.IntegerField('Niveau')

    def annee_en_cours(self):
        return self.annee_cours_dateint == timezone.datetime.today().year
    annee_en_cours.admin_order_field = 'annee_cours_dateint'
    annee_en_cours.short_description = 'année en cours'

    def __unicode__(self):
        return self.nom_etablissement_text+" "+str(self.niveau)+"eme, "+str(self.annee_cours_dateint)


#===============================================================================
# ELEVE
#===============================================================================
class Eleve(models.Model):
    """
    Definition d'un modèle d'élève
.    
    see API docs:
        https://docs.djangoproject.com/en/1.7/ref/contrib/auth/
        https://docs.djangoproject.com/en/1.7/topics/auth/default/#user-objects
    
    username
        Required. 30 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
    first_name
        Optional. 30 characters or fewer.
    last_name
        Optional. 30 characters or fewer.
    email
        Optional. Email address.
    password
        Required. A hash of, and metadata about, the password.
         (Django doesn’t store the raw password.) Raw passwords can be arbitrarily 
         long and can contain any character. See the password documentation.1
    """
    
    user = models.OneToOneField(User)
    
    ma_classe = models.ForeignKey(MesClasse)
    date_de_naissance = models.DateField()
    
    def __unicode__(self):
        return self.user.username
    
    #nom = models.CharField(max_length=30)
    #prenom = models.CharField(max_length=30)
    #courriel = models.EmailField()
    # mot_de_passe = models.CharField(max_length=32)
    #link to MesClasses
    

#===============================================================================
# SEQUENCE
#===============================================================================
class MesSequence(models.Model):
    """
    Classe définissant le modèle du chapitrage
    progression;...
    """
    short_description_sequence = models.CharField("Nom de la séquence", max_length=200)
    full_description_sequence = models.TextField("Description d'une séquence", default='Description manquante')
    niveau_indicatif = models.IntegerField('Niveau', blank=True, null=True)
    
    domaine = models.CharField("domaine et/ou thème", max_length=200)
    
    #link to MesClasses
    ma_classe = models.ForeignKey(MesClasse,blank=True, null=True)
   
    def __unicode__(self):
        try:
            return self.short_description_sequence+" niveau "+str(self.ma_classe.niveau)+"eme"
        except:
            return self.short_description_sequence
#===============================================================================
# SEANCES
#===============================================================================
class MesSeance(models.Model):
    """
    Classe définissant le modèle des séances
    Une séance références des activités
    activités; videos; exercices; 
    """
    short_description_seance = models.CharField("Objet de la séance", max_length=200)
    full_description_seance = models.TextField("Description d'une séance ", default='Description requise')
    #ressource_de_la_seance
    # http://code.google.com/p/django-selectreverse/
    
    #link to MesClasses
    ma_sequence = models.ForeignKey(MesSequence)
   
    def __unicode__(self):
        return self.short_description_seance
    
    
#===============================================================================
# ACTIVITE - FORMULAIRES - QUESTIONS - VIDEOS - DOCUMENTS
#===============================================================================
class MesActivite(models.Model):
    """
    Classe définissant le modèle des activités
    activités; videos; exercices;pdf...
    """
    short_description_activite = models.CharField("Type D'activité", max_length=200)
    full_description_activite = models.TextField("Enoncé ", default='Description requise pour cette activité')
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    
    ma_seance = models.ForeignKey(MesSeance)
    
    def __unicode__(self):
        return self.short_description_activite
    
    
           
       
       
       
       