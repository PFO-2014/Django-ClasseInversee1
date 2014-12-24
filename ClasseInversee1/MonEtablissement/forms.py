# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from MonEtablissement.models import Eleve

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field,\
    Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

#===============================================================================
# FORMULAIRE AJOUT ELEVE
#===============================================================================

class UserForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
                                
#     password = forms.CharField(label='Mot de passe', required=True, 
#                                widget = forms.PasswordInput())
    password = forms.CharField(label="Mot de passe",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Vérification du mot de passe",
                                widget=forms.PasswordInput)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        PrependedText('first_name', 
                      '<span class="glyphicon glyphicon-user"></span> ',  
                      css_class='input-sma'),
        PrependedText('last_name', 
                      '<span class="glyphicon glyphicon-user"></span> ',  
                      css_class='input-sma'),
        PrependedText('username', 
                      '<span class="glyphicon glyphicon-user"></span> ',  
                      css_class='input-sma'),
        PrependedText('email', 
                      '<span class="glyphicon glyphicon-envelope"></span> ', 
                      css_class='input-sm'),
#         PrependedText('password', 
#                       '<span class="glyphicon glyphicon-asterisk"></span> ', 
#                       css_class='input-sm'),
        PrependedText('password', 
                      '<span class="glyphicon glyphicon-asterisk"></span> ', 
                      css_class='input-sm'),
        PrependedText('password2', 
                      '<span class="glyphicon glyphicon-asterisk"></span> ', 
                      css_class='input-sm'),
                           
        FormActions(
            Submit('save', 'continue', css_class='btn-primary'),
        )
    )
    
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Veuillez entrer deux fois le même mot de passe')
                
        return password2
        
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class StudentProfileForm(forms.ModelForm):
    
   
    
    class Meta:
        model = Eleve
        fields = ('user','date_de_naissance', 'ma_classe')
        

    #Crispy FormHelper
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(                    
        PrependedText('date_de_naissance', 
                      '<span class="glyphicon glyphicon-user"></span> ',  
                      css_class='input-sma'),
        PrependedText('ma_classe', 
                      '<span class="glyphicon glyphicon-home"></span> ', 
                      css_class='input-sm'),
        Field('user', type='hidden'),
       
        
        
        FormActions(
            Submit('save', 'continue', css_class='btn-primary'),
        )
    )
   

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class MessageForm(forms.Form):
    
    text_input = forms.CharField()
     
    textarea = forms.CharField(
    widget = forms.Textarea(),
    )
     
    radio_buttons = forms.ChoiceField(
    choices = (
    ('option_one', "Option one is this and that be sure to include why it's great"),
    ('option_two', "Option two can is something else and selecting it will deselect option one")
    ),
    widget = forms.RadioSelect,
    initial = 'option_two',
    )
     
    checkboxes = forms.MultipleChoiceField(
    choices = (
    ('option_one', "Option one is this and that be sure to include why it's great"),
    ('option_two', 'Option two can also be checked and included in form results'),
    ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
    ),
    initial = 'option_one',
    widget = forms.CheckboxSelectMultiple,
    help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    )
     
    appended_text = forms.CharField(
    help_text = "Here's more help text"
    )
     
    prepended_text = forms.CharField()
     
    prepended_text_two = forms.CharField()
     
    multicolon_select = forms.MultipleChoiceField(
    choices = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
    )
     
    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-vertical'
    helper.layout = Layout(
    Field('text_input', css_class='input-xlarge'),
    Field('textarea', rows="3", css_class='input-xlarge'),
    'radio_buttons',
    Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
    AppendedText('appended_text', '.00'),
    PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
    PrependedText('prepended_text_two', '@'),
    'multicolon_select',
    FormActions(
    Submit('save_changes', 'Save changes', css_class="btn-primary"),
    Submit('cancel', 'Cancel'),
    )
    ) 
    
class LoginForm(forms.Form):
    #email = forms.EmailField(label='Courriel')
    username = forms.CharField(label='Nom Utilisateur', required=True)
    password = forms.CharField(label='Mot de passe', required=True, 
                               widget = forms.PasswordInput)
    remember = forms.BooleanField(label='Se souvenir de moi', required=False)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        PrependedText('username', 
                      '<span class="glyphicon glyphicon-user"></span> ',  
                      css_class='input-sma'),
        PrependedText('password', 
                      '<span class="glyphicon glyphicon-asterisk"></span> ', 
                      css_class='input-sm'),
        FormActions(
            Submit('login', 'Connexion', css_class='btn-primary'),
        )
    )
#     helper.add_input(Submit('login', 'Connexion', css_class='btn-primary'))
    
    
    
    
    
    def clean(self):
        """
        surcharge de la méthode clean de form.Form
        la méthode clean effectue le transtypage html, django vers python
        """
        #appel de clean au niveau de la classe parente. ie: non encore surchargé
        cleaned_data = super (LoginForm, self).clean()
        #email_u = cleaned_data.get("email")
        username_u = cleaned_data.get("username")
        password_u = cleaned_data.get("password")
        # Vérifie que les deux champs sont valides
        qresult = User.objects.filter(username=username_u).values('password')
        if len(qresult) != 1:
            raise forms.ValidationError("Nom Utilisateur ou mot de passe erroné.")
        if not check_password(password_u, qresult[0]['password'] ):
            raise forms.ValidationError("Nom Utilisateur ou mot de passe erroné.")
   
        return cleaned_data
        
        
class QuestionForm(forms.Form):
    """
    Formulaire pour une question unique
    """
    
    def __init__(self, question, reponse , *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
         
        self.question = question
        self.reponse = reponse
        
        # Uni-form
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.layout =  Layout(
                                     
                Field(self.question.enonce, style=" padding: 10px;"),
                Field('question_eleve'),
                FormActions(
                            Submit('save_changes', 'Save changes', css_class="btn-primary"),
                            Submit('cancel', 'Cancel'),
                            )                   
                )
#         self.helper.add_input(Submit('submit', 'Submit'))
    
         
        #prepare a radio-button list
        self.answerlist = self.get_questiontext()
        self.fields[self.question.enonce] = forms.ChoiceField(
                                                        choices =self.answerlist, 
                                                        widget = forms.RadioSelect,
                                                        )
        #dummy textarea for student personal question
        self.fields['question_eleve'] = forms.CharField(
                                        widget = forms.Textarea(),
                                        )

  
        
    def get_questiontext(self, reponse=None):
        """
        build a list of question
        """
        
        if reponse is None:
        
            reponse = self.reponse
            
        questionlist = []
        for i,q in enumerate(reponse):
            questionlist.append((str(i),str(q.reponse_text),))
     
        return questionlist
            
        
    
    
    