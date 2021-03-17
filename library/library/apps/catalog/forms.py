from django import forms  
from .models import UserProfile, Book
  
class BookForm(forms.ModelForm):  
    class Meta:  
        model = Book  
        fields = '__all__'

class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = ['age']