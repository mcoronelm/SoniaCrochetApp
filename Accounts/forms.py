from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get the currently active user model (Accounts.User)
User = get_user_model()

class ClientRegisterForm(UserCreationForm):
    # Field to collect email address
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] + list(UserCreationForm.Meta.fields)
    

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Ensure the custom is_client field is set to True
        user.is_client = True 
        
        # Set the email field from the form data
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user