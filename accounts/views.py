from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm, UpdateForm, NotiForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        u_form = UpdateForm(request.POST, instance=user_obj)
        n_form = NotiForm(request.POST, instance=user_obj.profile)
        if u_form.is_valid() and n_form.is_valid():
            u_form.save()
            n_form.save()
            
            return redirect('my_account')
    else:
        u_form = UpdateForm(instance=user_obj)
        n_form = NotiForm(instance=user_obj)

    context = {
        'u_form': u_form,
        'n_form': n_form
    }

    return render(request, 'my_account.html', context)
