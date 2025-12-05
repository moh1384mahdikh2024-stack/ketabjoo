from django import forms
from django.contrib.auth import get_user_model

MyUSer = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Username',
                'id': 'floatingUsername',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Password',
                'id': 'floatingPassword',
            }
        ),
        label='گذرواژه',
        max_length=128)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = MyUSer
        fields = ('username', 'email', 'password', 'phone', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-start', 'id': 'floatingUsername'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control text-start', 'id': 'floatingPassword'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-start', 'id': 'floatingEmail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control text-start', 'id': 'floatingPhone'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control text-start', 'id': 'floatingFirstName'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control text-start', 'id': 'floatingLastName'}),
        }


class RegisterForm(forms.Form):
    username = forms.CharField(
        min_length= 5,
        max_length=150,
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Username',
                'id': 'floatingUsername',
            }
        )
    )
    password = forms.CharField(
        min_length=8,
        max_length=128,
        label="گذرواژه",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Password',
                'id': 'floatingPassword',
            }
        ),
    )
    confirm_password = forms.CharField(
        min_length=8,
        max_length=128,
        label="تکرار گذرواژه",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Confirm Password',
                'id': 'floatingConfirmPassword',
            }
        )
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                'class':'form-control text-start',
                'placeholder': 'Email',
                'id': 'floatingEmail',
            }
        )
    )
    phone = forms.CharField(
        min_length=11,
        max_length=11,
        label="شماره تلفن",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Phone',
                'id': 'floatingPhone',
            }
        )
    )
    first_name = forms.CharField(
        max_length=150,
        label="نام",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'First Name',
                'id': 'floatingFirstName',
            }
        )
    )
    last_name = forms.CharField(
        max_length=150,
        label="نام خانوادگی",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-start',
                'placeholder': 'Last Name',
                'id': 'floatingLastName',
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = MyUSer.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError("این نام کاربری در سایت وجود دارد")
        return username

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("گذرواژه با تکرار آن مطابقت ندارد")
        return data