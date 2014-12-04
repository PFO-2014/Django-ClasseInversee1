# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from django.template import RequestContext

from django.utils import timezone

from MonEtablissement.models import MesActivite, MesClasse, MesSeance,\
                                    MesSequence
from forms import LoginForm

# Create your views here.

#===============================================================================
# Creation de la vue Index sur les Niveaux
#===============================================================================
# # 1. Codage dur pour test initiaux
# def index(request):
#     """
#     Main Index Page: Expose only current year MesClasse.niveau
#     """
#     current_year_classes_list = MesClasse.objects.filter(annee_cours_dateint=timezone.datetime.today().year).order_by("-niveau")
#  
#     output =', '.join([str(classe.niveau)+"eme" for classe in current_year_classes_list])
#     return HttpResponse(output)
    
# 2. Codage raccourci avec méthode render()
def index(request, *args):
    """
    Main Index Page: Expose only current year MesClasse.niveau
    """
    
    
    current_year_classes_list = MesClasse.objects.filter(annee_cours_dateint=timezone.datetime.today().year).order_by("-niveau")
    context = {'current_year_classes_list': current_year_classes_list}
    
    try:
        email = request.POST['email']
        context.update({'email':email})
    except:
        pass
    
    #render(objet requête, garabit, contexte rempli <dict> (variable))
    return render(request, 'MonEtablissement/index.html', context)

def sequence(request, etablissement_text, niveau_int):
    """
    View all (current year) sequences for a unique level
    """
    
#     sequence_list = MesSequence.objects.filter(ma_classe=classe_id)
    context = { 'etablissement_text': etablissement_text, 'niveau_int':niveau_int}
    #render(objet requête, garabit, contexte rempli <dict> (variable) **kwargs)
    return render(request, 'MonEtablissement/sequence.html', context)
#     output ="you are looking sequences at "+unicode(etablissement_text)+" niveau "+niveau_int+" eme" 
#     return HttpResponse(output)

# def login(request):
#     """
#     Renvoi vers ?
#     """
#     context = {}
#     
#     if len(request.POST) >0:
#         #test parameters validity
#         if 'email' not in request.POST or 'password' not in request.POST:
#             context['error'] = "Veuillez entrer une adresse de courriel et un mot de passe."
#             return render(request, 'MonEtablissement/login.html', context)
#         else:
#             email = request.POST['email'] 
#             password = request.POST['password']
#             # Teste si le mot de passe est le bon
#             if password != 'sesame' or email != 'pierre@lxs.be':
#                 context['error'] = "Adresse de courriel ou mot de passe erroné."
#                 return render(request,'MonEtablissement/login.html', context)
#             # Tout est bon, on va à la page d'accueil
#             else:
#                 return HttpResponseRedirect('/welcome')
#     # Le formulaire n'a pas été envoyé
#     else:
#         return render(request, 'MonEtablissement/login.html')
        

def login(request):
    """
    Méthode qui instancie un formulaire de login 
    OU
    Vérifie que les id. de connexion ont été entrés correctement avant redirection vers /welcome
    """
    form = LoginForm()
    if (request.method == 'POST'):
        #recup. le POST et le passe dans un objet formulaire pour 
        #faire usage de form.is_valid
        #OU
        #construit empty form pour redemander les id. connexion
        form = LoginForm(request.POST or None)
        if form.is_valid():
            return HttpResponseRedirect('/welcome')
    return render(request,'MonEtablissement/login.html', {'form': form})


def welcome(request):
    """
    Renvoi vers ?
    """
    return index(request)


    
    