from django import forms
from .models import CustomUser
from django.core.validators import FileExtensionValidator


class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'username_required': ("User name is a required field."),
        'valid_images': {"Image uploaded is not in valid form, must be in png or jpg format!"}
    }
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=("Enter the same password as above, for verification."))
    username = forms.CharField(label=("Please Enter Username"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=("Please Enter Your Email"),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.FileField(label=("Please Upload Your Profile Image"),
                                    widget=forms.FileInput(attrs={'class': 'form-control'}),
                                    validators=[FileExtensionValidator(['png', 'jpg'])])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_user_name(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(
                self.error_messages['username_required'],
                code='username_required'
            )
        return username

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user