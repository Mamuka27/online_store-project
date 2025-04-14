from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import EditProfileForm

from django.contrib.auth.forms import UserChangeForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm

@login_required
def profile(request):
    return render(request, 'user/profile.html')

class CustomLoginView(LoginView):
    template_name = 'user/login.html'

def custom_logout(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('item_list')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'user/edit_profile.html'
    success_url = reverse_lazy('account_profile')

    def get_object(self):
        return self.request.user