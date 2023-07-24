from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


class UserRegisterView(CreateView):
    template_name = "users/register.html"
    success_url = "/"
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        response = super().form_valid(form)

        form.save()
        curr_user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        # logs in the user after account is created
        login(self.request, curr_user)
        messages.success(self.request, "You're logged in")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("Context:", context)
        context["title"] = "Register"
        return context


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Account Updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"user_form": user_form, "profile_form": profile_form, "title": "Profile"}
    return render(request, "users/profile.html", context)
