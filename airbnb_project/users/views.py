from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from users import models as users_model
from users import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, template_name="users/login.html", context={"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user != None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, template_name="users/login.html", context={"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


# class LoginView(FormView):
#     form_class=forms.LoginForm
#     success_url=reverse_lazy("core:home")  #doc-Using the Django authentication system
#     template_name="users/login.html"

#     def form_valid(self,form):
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         user = authenticate(self.request, username=email, password=password)
#         if user != None:
#             login(self.request, user)
#         return super().form_valid(form)


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
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Hello"] = "Hello"
        return context


class UpdateProfileView(UpdateView):
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

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)  # intercept the email and
    #     # put it into username
    #     # Error occured

    def get_object(self, queryset=None):
        return self.request.user


class UpdatePasswordView(PasswordChangeView):
    template_name = "users/update-password.html"
