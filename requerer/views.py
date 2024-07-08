from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
    }

    return render(request, 'requerer/new_request.html', context)
