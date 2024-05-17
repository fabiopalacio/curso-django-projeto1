from django.http import Http404
from django.shortcuts import redirect, render  # type: ignore
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import RegisterForm, LoginForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create'),
        'btn_text': 'Send...'
    })


def register_create(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Your user was created. Please, log in")

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login_view.html', context={
        'form': form,
        'form_action': reverse('authors:login_auth'),
        'btn_text': 'Login'

    })


def login_create(request):

    if not request.POST:
        raise Http404()

    login_url = reverse('authors:login')
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticate_user is not None:

            messages.success(request, 'You are logged in.')
            login(request, authenticate_user)
        else:
            messages.warning(request, "Invalid credentials.")
    else:
        messages.error(request, "Invalid credentials.")

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('recipes:home'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('recipes:home'))

    logout(request)
    messages.success(request, 'Logout successfully')
    print('Logout')
    return redirect(reverse('recipes:home'))
