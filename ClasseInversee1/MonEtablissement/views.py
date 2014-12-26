# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf

from django.template import RequestContext

from django.utils import timezone

from MonEtablissement.models import MesActivite, MesClasse, MesSeance,\
                                    MesSequence, MesNiveaux, User, Eleve, \
                                    MesQuestion, MesReponse
from forms import LoginForm, MessageForm, StudentProfileForm, UserForm, QuestionsForm

# Create your views here.

#===============================================================================
# Creation de la vue Index sur les Niveaux
#===============================================================================
#  2. Codage raccourci avec méthode render()
def index(request, logged_user=None, *args):
    """
    Main Index Page: Expose only current year MesClasse.niveau
    """
    
    current_year_classes_list = MesClasse.objects.filter(annee_cours_dateint=timezone.datetime.today().year).order_by("niveau")
    niveau_list = MesNiveaux.objects.filter()
    context = {'current_year_classes_list': current_year_classes_list, 'niveau_list': niveau_list}
    
    try:
        email = request.POST['email']
        context.update({'email':email})
    except:
        pass
    
    if logged_user:
        context.update({'logged_user': logged_user})
    
    #render(objet requête, garabit, contexte rempli <dict> (variable))
    return render(request, 'MonEtablissement/index_bs.html', context)

def sequence(request, niveau_int):
    """
    View all (current year) sequences for a unique level
    """
    
#     sequence_list = MesSequence.objects.filter(ma_classe=classe_id)
    context = {'niveau_int':niveau_int}
    #render(objet requête, garabit, contexte rempli <dict> (variable) **kwargs)
    return render(request, 'MonEtablissement/sequence.html', context)
#     output ="you are looking sequences at "+unicode(etablissement_text)+" niveau "+niveau_int+" eme" 
#     return HttpResponse(output)


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
            #Recupère le nom d'utilisateur renseigné par l'utilisateur dans le LoginForm
            user_name = form.cleaned_data['username'] 
            #Recupere l'entrée correspondante dans le modèle User
            logged_user = User.objects.get(username=user_name) 
            #Passe l'identificateur à l'objet request 
            request.session['logged_user_id'] = logged_user.id 
            return HttpResponseRedirect('/welcome')
    return render(request,'MonEtablissement/login.html', {'form': form})


def get_logged_user_from_request(request):
    """
    Protection des pages privées 
    
    TODO: distinguer les connexions eleves/professeur pour proposer une 
          page d'administration professeur
    """
    
    if 'logged_user_id' in request.session: 
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
        return logged_user
    else:
        return None
    
    
def show_profile(request):
    """
    Creation d'une vue pour afficher le profil utilisateur
    """
    logged_user = get_logged_user_from_request(request)
    if logged_user:
        return render_to_response ('MonEtablissement/show_profile.html',
                                   {'user_to_show': logged_user})
    # Le paramètre n'a pas été trouvé
    else:
        return HttpResponseRedirect('/login')

def welcome(request):
    """
    Renvoi vers page d'acceuil avec identification
    """
    logged_user = get_logged_user_from_request(request)
    
    if logged_user:
        return index(request, logged_user=logged_user)
    #kept for reference - replaced by the generic get_logged_user_from_request()
#     if 'logged_user_id' in request.session:
#         logged_user_id = request.session['logged_user_id']
#         logged_user = User.objects.get(id=logged_user_id)
#         return index(request, logged_user=logged_user)

    else:
        return HttpResponseRedirect('/login')
    
    


def exampleform(request):
    """
    test crispy forms
    """
    # This view is missing all form handling logic for simplicity of the example
    return render(request, 'MonEtablissement/exampleform.html', {'form': MessageForm()}) 


def register(request):
    """
    User registration
    """
       
    if len(request.POST) > 0:
        
        
        # Create form instances from POST data or build empty ones
        if 'password' in request.POST:
            user_form = UserForm(request.POST)
            student_form = StudentProfileForm()
        if 'ma_classe' in request.POST:
            student_form = StudentProfileForm(request.POST)
            user_form = UserForm()
            
        if user_form.is_valid():
            
            # Save a new User object from the form's data.
            user_form.save()
            # Retrieve the username from the last POST
            username = request.POST.get('username')
            #Retrieve the underlying User object from DB
            user = User.objects.get(username=username)
            #Create an non-validating object
            eleve = student_form.save(commit=False)
            #Pass it the desired user foreign key
            eleve.user = user
            #build a new "partial + Non validated" StudentProfileForm using the eleve instance
            student_form = StudentProfileForm(None, instance=eleve)
            return render(request,'MonEtablissement/user_profile.html', {'student_form': student_form, 'username': str(student_form.helper.attrs)})
        
        elif student_form.is_valid():
            
            student_form.save(commit=True)
            return HttpResponseRedirect('/login')
        
        elif not user_form.has_changed() and not user_form.is_valid() and user_form.is_bound :
            #user_form: Case not valid, including empty form
            return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form}) 
        
        elif not student_form.is_valid() and student_form.is_bound :
            
            return render (request, 'MonEtablissement/user_profile.html', {'student_form': student_form})
            
        else:
            return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form})
    else:
        user_form = UserForm()
        student_form = StudentProfileForm()
        
        return render (request, 'MonEtablissement/user_profile.html', {'user_form': user_form, 'student_form': student_form})

def iterquestions():
    """
    generator pour iterer sur un set de question/reponse
    http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
    """
    #get a random question
    questions = MesQuestion.objects.order_by('?')
    
    for question in questions:
        reponse = MesReponse.objects.select_related().filter(question = question)
        yield question, reponse


def my_questionform(request):
    """
    Classe pour instancier un formulaire de question/reponse
    """
    #prepare a form; QCM

    form = QuestionsForm()
    for question, reponse in iterquestions():
        form.add_question(question, reponse)
    form.close()
    
    return render(request, 'MonEtablissement/questionform.html', {'form': form})
    

        

    