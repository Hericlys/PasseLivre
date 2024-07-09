from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requerer.models import Request


def home(request):
    context = {
        'page_settings': {
            'title': 'Home',
        }   
    }

    return render(request, 'requerer/home.html', context)


@login_required(login_url="accounts:login")
def new_request(request):
    context = {
        'page_settings': {
            'title': 'Novo requerimento',
        },
        'forms_choices': {
            'sexo': Request.SEXO_CHOICES,
            'raca': Request.RACA_COR_CHOICES,
            'sangue': Request.SANGUE_CHOICES,
            'uf': Request.UF_CHOICES,
            'cid': Request.CID_CHOICES,
            'deficiencia': Request.TIPO_DEFICIENCIA_CHOICES,
        }
    }

    return render(request, 'requerer/new_request.html', context)
