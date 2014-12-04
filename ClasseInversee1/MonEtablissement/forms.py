# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    
    
class LoginForm(forms.Form):
    #email = forms.EmailField(label='Courriel')
    username = forms.CharField(label='Nom Utilisateur', required=True)
    password = forms.CharField(label='Mot de passe', required=True, 
                               widget = forms.PasswordInput)
    remember = forms.BooleanField(label='Se souvenir de moi')
    
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
        
        