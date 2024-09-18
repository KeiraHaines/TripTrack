from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Trip, Destination, Transport, TripLeg

class CreateUserForm(UserCreationForm):
    """
    Custom user creation form extending Django's UserCreationForm.
    Includes email field and custom styling for form fields.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        """
        Custom email validation to ensure uniqueness.
        """
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        """
        Override save method to include email field.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EventFormTrans(forms.ModelForm):
    """
    Form for creating or updating a TripLeg, including destination and transport.
    """
    strLoc = forms.CharField(
        max_length=49,  
        widget=forms.TextInput(attrs={'placeholder': 'Destination', 'maxlength': '49'}),
        required=True
    )
    strTran = forms.ModelChoiceField(
        queryset=Transport.objects.all(),  
        widget=forms.Select(),
        required=True  
    )

    class Meta:
        model = TripLeg
        fields = ['strLoc', 'strTran']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['strTran'].empty_label = None  # Removes the empty label from transport choices

class newTripForm(forms.ModelForm):
    """
    Form for creating a new Trip, including name and date range.
    """
    class Meta:
        model = Trip
        fields = ['strTripName', 'intStartDate', 'intEndDate']
        widgets = {
            'strTripName': forms.TextInput(attrs={'placeholder':'    Name of Trip'}),
            'intStartDate': forms.DateInput(attrs={'type': 'date'}),
            'intEndDate': forms.DateInput(attrs={'type': 'date'}),
        }

class BaggageCheckForm(forms.Form):
    """
    Simple form for checking luggage weight.
    """
    intLuggageWeight = forms.DecimalField(label='Enter a Number', required=True)