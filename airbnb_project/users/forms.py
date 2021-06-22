from django import forms
from users import models as users_model


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

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
            user = users_model.User.objects.get(username=email)  # compare
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

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def save(self, *args, **kwargs):
        user = super().save(commit=False)  # create object
        print(self.cleaned_data)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
