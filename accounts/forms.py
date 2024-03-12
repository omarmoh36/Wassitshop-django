from django import forms
from .models import Account



class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password','confirm_password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'enter first_name'
        self.fields['last_name'].widget.attrs['placeholder']= 'enter last_name'
        self.fields['phone_number'].widget.attrs['placeholder']= 'enter your phone_number'
        self.fields['email'].widget.attrs['placeholder']= 'enter your address email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'
    def clean (self):
        cleened_data= super(RegistrationForm,self).clean()
        password= cleened_data.get('password')
        confirm_password= cleened_data.get('confirm_password')
        if password != confirm_password :
            raise forms.ValidationError(
                "Password is does not match"
            )
