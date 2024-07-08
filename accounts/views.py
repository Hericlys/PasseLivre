from django.shortcuts import render, redirect
from utils import validators as va
from utils.rands import random_letters
from accounts.models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings


def register(request):
    context = {
        'page_settings': {
            'title': 'Register',
        }
    }

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        try:
            user = CustomUser.objects.get(email=email)
            if user.is_check:
                messages.warning(request, 'E-mail já registrado, faça login')
                return redirect('accounts:login')
            else:
                messages.warning(request, 'E-mail já registrado, verifique seu E-mail')
                return redirect('accounts:check_email')
        except CustomUser.DoesNotExist:
            pass

        context.update({
            'form_values': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
        })

        is_valid = True

        if not va.min_characters(first_name, 2):
            is_valid = False
            messages.error(
                request,
                'Nome precisa ter no mínimo 2 caracteres'
            )

        if not va.max_characters(first_name, 30):
            is_valid = False
            messages.error(
                request,
                'Nome só pode ter no maximo 30 caracteres'
            )

        if not va.min_characters(last_name, 2):
            is_valid = False
            messages.error(
                request,
                'Sobrenome precisa ter no mínimo 2 caracteres'
            )

        if not va.max_characters(last_name, 30):
            is_valid = False
            messages.error(
                request,
                'sobreome só pode ter no maximo 30 caracteres'
            )

        try:
            validate_email(email)
            user = CustomUser.objects.get(email=email)
            # verificar se o e-mail já existe em nosso sistema
        except ValidationError:
            is_valid = False
            messages.error(request, 'E-mail invalido, tente outro.')

        is_strong_password, message = va.is_strong_password(password)
        if not is_strong_password:
            is_valid = False
            messages.error(request, message)


        if password != password2:
            is_valid = False
            messages.error(
                request,
                'As senhas não conferem, tente novamente'
            )

        if is_valid:
            new_user = CustomUser.objects.create(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            # send e-mail
            html_content = render_to_string(
                'accounts/emails/check_email.html',
                {
                    'token': new_user.token,
                }
            )

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                'Confirmação de E-mail',
                text_content,
                settings.EMAIL_HOST_USER,
                [f'{email}',]
            )

            email.attach_alternative(html_content, 'text/html')
            email.send()

            messages.success(
                request,
                'Conta criada! Verifique seu E-mail para obter o token de atentificação'
            )
            # redirecionar para o next
            return redirect("requerer:new_request")

    return render(request, 'accounts/register.html', context)


def check_email(request):
    context = {
        'page_settings': {
            'title': 'Verificação de E-mail',
        }
    }

    if request.method == "POST":

        email = request.POST.get('email')

        context.update({
            'form_values': {
                'email': email,
            },
        })

        d1 = request.POST.get('d1')
        d2 = request.POST.get('d2')
        d3 = request.POST.get('d3')
        d4 = request.POST.get('d4')
        d5 = request.POST.get('d5')
        d6 = request.POST.get('d6')

        token = d1 + d2 + d3 + d4 + d5 + d6
        try:
            user = CustomUser.objects.get(email=email)

            if user.is_check:
                messages.warning(request, 'E-mail já verificado, faça login')
                return redirect('accounts:login')

            if token == user.token:
                user.is_check = True
                user.token = random_letters(6)
                user.save()
                messages.success(
                    request,
                    'E-mail confirmado com sucesso!, agora faça login'
                )
                return redirect('accounts:login')
            else:
                messages.error(request, 'Token invalido, tente novamente')
        except CustomUser.DoesNotExist:
            messages.erro(request, 'Não exitem solicitações para esse E-mail')

    return render(request, 'accounts/check_email.html', context)


def login_view(request):
    context = {
        'page_settings': {
            'title': 'Login',
        }
    }

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:register') #modificar para home do site
        else:
            messages.error(request, 'Credenciais invalidas')
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')