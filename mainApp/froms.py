from django import forms
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationForm(ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a password'
        }),
        validators=[validate_password]  # Uses Django's built-in password validators
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your university ID'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
        }
        labels = {
            'username': 'University ID',
            'email': 'Email Address'
        }
        
    def clean(self):
        """
        Validates that the password entries match
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
            
        return cleaned_data
        
    def save(self, commit=True):
        # Save the user without committing to the database
        user = super().save(commit=False)
        # Set the password properly (this handles hashing)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user