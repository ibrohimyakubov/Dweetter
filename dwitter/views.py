from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, Dweet
from .forms import DweetForm, SignUpForm


@login_required(login_url='dwitter:login')
def dashboard(request):
    tweet = Dweet.objects.filter(user=request.user).order_by("-created_at")
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets, 'tweets': tweet},
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    dweet = Dweet.objects.filter(user_id=profile.pk).order_by('-created_at')
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, "dwitter/profile.html", {"profile": profile, 'dweets': dweet})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Your account has been created!')

            return redirect('dwitter:dashboard')
        else:
            messages.warning(request, form.errors)
            return redirect('dwitter:register')

    form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'user/register.html', context)


def login_(request):
    if request.user.is_authenticated:
        return redirect('dwitter:dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dwitter:dashboard')
        else:
            messages.warning(request, "Login Error, Try again or Sign Up!")
            return redirect('user:login')
    return render(request, 'user/login.html')


@login_required
def logout_func(request):
    logout(request)
    return redirect('dwitter:login')
