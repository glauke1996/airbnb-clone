from django import forms
from django.forms import fields, widgets
from users import models as users_model


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         users_model.User.objects.get(username=email)
    #     except users_model.User.DoesNotExist:
    #         raise forms.ValidationError("UserDoesNotExist")
    #     print(self.cleaned_data)
    #     return "lala"

    def clean(self):
        email = self.cleaned_data.get("email")  # from input
        password = self.cleaned_data.get("password")
        try:
            user = users_model.User.objects.get(
                username=email
            )  # compare #This is how to get an user object!!
            if user.check_password(
                password
            ):  # check_password compare each encrypted password.
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("ps is wrong."))
        except users_model.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist."))


# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())
#     password1 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             users_model.User.objects.get(username=email)
#             raise forms.ValidationError("Duplicated Username")
#         except users_model.User.DoesNotExist:
#             return email

#     def clean_password1(self):
#         print(self.cleaned_data)
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")

#         if password != password1:
#             raise forms.ValidationError("Password is wrong.")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         user = users_model.User.objects.create_user(email, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()  # which is the method of form.


class SignUpForm(forms.ModelForm):
    class Meta:
        model = users_model.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First_name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last_name"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password_confirm"}),
        label="Confirm Password",
    )

    def save(self, *args, **kwargs):
        user = super().save(commit=False)  # create object
        # print(self.cleaned_data)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


class UpdateForm(forms.ModelForm):
    class Meta:
        model = users_model.User
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "gender",
            "bio",
            "birthdate",
            "language",
            "currency",
            # "email",
        )
        widgets = {
            "birthdate": forms.TextInput(attrs={"placeholder": "0000-00-00"}),
            "email": forms.TextInput(attrs={"placeholder": "Existing Email"}),
        }

    # New_email = forms.CharField(
    #     widget=forms.TextInput(attrs={"placeholder": "New Email"})
    # )


#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         avatar = self.cleaned_data.get("avatar")
#         gender = self.cleaned_data.get("gender")
#         bio = self.cleaned_data.get("bio")
#         birthdate = self.cleaned_data.get("birthdate")
#         language = self.cleaned_data.get("language")
#         currency = self.cleaned_data.get("currency")
#         New_email = self.cleaned_data.get("New_email")

#         user = users_model.User.objects.get(username=email,first_name=first_name)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.avatar = avatar
#         user.gender = gender
#         user.bio = bio
#         user.birthdate = birthdate
#         user.language = language
#         user.currency = currency
#         print(self.cleaned_data)
#         if New_email != None:
#             user.username = New_email
#         user.save()
