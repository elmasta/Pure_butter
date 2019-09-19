from django import forms

class CreateUser(forms.Form):
    login = forms.CharField(
        label='Pseudo',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Pseudo"}),
        required=True
        )
    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder": "Email"}),
        required=True
        )
    password = forms.CharField(
        label='Mot de Passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Mot de passe"}),
        max_length=50
        )
