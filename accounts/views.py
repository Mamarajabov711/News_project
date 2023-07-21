from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm, UserRegisterForm
# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Kirish muvaffaqiyatli amalga oshirildi")
                else:
                    return HttpResponse("Sizning profilingiz faol holatda emas ")

            else:
                return HttpResponse("Login yoki Parolda xatolik bor")
    else:
        form = LoginForm()
        context = {
            "form":form
        }

    return render(request, 'registration/login.html', context)

def dashboard_view(request):
    user = request.user
    context = {
        'user': user
    }

    return render(request, 'pages/user_profile.html', context)





def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegisterForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'account/register.html', context)




class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'
