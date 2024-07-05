from django.shortcuts import render, redirect
from utils import validators as va
from accounts.models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
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

            return redirect("accounts:login")

    return render(request, 'accounts/register.html', context)


def check_email(request):
    context = {
        'page_settings': {
            'title': 'Verificação de E-mail',
        }
    }

    return render(request, 'accounts/check_email.html', context)


def login(request):
    context = {
        'page_settings': {
            'title': 'Login',
        }
    }

    return render(request, 'accounts/login.html', context)