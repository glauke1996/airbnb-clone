from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from users import models as users_model
from users import forms, mixins


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm()
#         return render(request, template_name="users/login.html", context={"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user != None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, template_name="users/login.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class LoginView(mixins.LoggedOutOnlyView, FormView):
    form_class = forms.LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user != None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg != None:
            return next_arg
        else:
            return reverse("core:home")


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user != None:
            login(self.request, user)
        return super().form_valid(form)


class UserProfileView(DetailView):
    model = users_model.User
    context_object_name = "user_obj"  # user found on the view-> user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Hello"] = "Hello"
        return context


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = users_model.User
    template_name = "users/update_profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Updated"

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_object(self, queryset=None):  # return the object we want to edit
        return self.request.user

    def get_form(self, form_class=forms.UpdateForm):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        return form

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)  # intercept the email and
    #     # put it into username
    #     # Error occured


# class UpdateProfileView(FormView):
#     template_name = "users/update_profile.html"
#     form_class = forms.UpdateForm
#     success_url = reverse_lazy("core:home")

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class UpdatePasswordView(PasswordChangeView):
    template_name = "users/update-password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current_password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New_password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm_new_password"
        }
        return form
