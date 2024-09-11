from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from .models import newTrip, Destination, Transport, Leg

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class EventFormTrans(forms.ModelForm):
    destination = forms.CharField(
        max_length=49,  # Ensure this matches the max_length in the model
        widget=forms.TextInput(attrs={'placeholder': 'Destination', 'maxlength': '49'}),
        required=True
    )
    transport = forms.ModelChoiceField(
        queryset=Transport.objects.all(),  # Assuming Transport is a model
        widget=forms.Select(),
        required=True  # Make this field compulsory
    )

    class Meta:
        model = Leg
        fields = ['destination', 'transport']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transport'].empty_label = None


class newTripForm(forms.ModelForm):
    
    class Meta:
        model = newTrip
        fields = ['strTripName', 'intStartDate', 'intEndDate']
        widgets = {
            'strTripName': forms.TextInput(attrs={'placeholder':'    Name of Trip'}),
            'intStartDate': forms.DateInput(attrs={'type': 'date'}),
            'intEndDate': forms.DateInput(attrs={'type': 'date'}),
        }

class BaggageCheckForm(forms.Form):
    number = forms.DecimalField(label='Enter a Number', max_digits=5, decimal_places=2, required=True)

