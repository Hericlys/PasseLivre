from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requerer.models import Request
from utils.validators import validate_cpf
from utils.data_processing import clean_space
from django.contrib import messages
from requerer.models import Request, Documents
from accounts.models import CustomUser


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

    if request.method == "POST":
        name = clean_space(request.POST.get('full-name'))
        cpf = request.POST.get('cpf')
        d_nascimento = request.POST.get('d-nascimento')
        sexo = request.POST.get('sexo')
        rg = request.POST.get('rg')
        emissor = clean_space(request.POST.get('emissor'))
        uf_rg = request.POST.get('uf-rg')
        l_nascimento = clean_space(request.POST.get('l-nascimento'))
        raca = request.POST.get('raca')
        sangue = request.POST.get('sangue')
        n_mae = clean_space(request.POST.get('n-mae'))
        n_pai = clean_space(request.POST.get('n-pai'))
        t_cid = request.POST.get('t-cid')
        cid = clean_space(request.POST.get('cid'))
        deficiencia = request.POST.get('deficiencia')
        telefone = request.POST.get('telefone')
        cep = request.POST.get('cep')
        logradouro = clean_space(request.POST.get('logradouro'))
        numero = request.POST.get('numero')
        cidade = request.POST.get('cidade')
        bairro = clean_space(request.POST.get('bairro'))
        uf_endereco = request.POST.get('uf-endereco')
        complemento = clean_space(request.POST.get('complemento'))

        if validate_cpf(cpf):
            try:
                user = CustomUser.objects.get(email=request.user.email)
            except:
                print(f'user não localizado por ----{request.user.email}----')

            new_request = Request(
                nome_completo=name, cpf=cpf, data_nascimento=d_nascimento,
                nome_mae=n_mae, nome_pai=n_pai, orgao_emissor=emissor,
                uf_rg=uf_rg, rg=rg, local_nascimento=l_nascimento, sexo=sexo,
                raca_cor=raca, tipo_sanguineo=sangue, telefone=telefone,
                deficiencia_tipo_cid=t_cid, deficiencia_cid=cid,
                deficiencia_tipo=deficiencia, cep=cep, logradouro=logradouro,
                numero=numero, complemento=complemento, bairro=bairro,
                cidade=cidade, uf=uf_endereco, user=user
            )
            new_request.save()
            messages.success(request, 'Requerimento realizado com sucesso')
        else:
            messages.error(request, 'CPF invalido')
            context.update({
                'form_values': {
                    'name': name,
                    'd_nascimento': d_nascimento,
                    'sexo': sexo,
                    'rg': rg,
                    'emissor': emissor,
                    'uf_rg': uf_rg,
                    'l_nascimento': l_nascimento,
                    'raca': raca,
                    'sangue': sangue,
                    'n_mae': n_mae,
                    'n_pai': n_pai,
                    't_cid': t_cid,
                    'cid': cid,
                    'deficiencia': deficiencia,
                    'telefone': telefone,
                    'cep': cep,
                    'logradouro': logradouro,
                    'numero': numero,
                    'cidade': cidade,
                    'bairro': bairro,
                    'uf_endereco': uf_endereco,
                    'complemento': complemento
                }
            })

    return render(request, 'requerer/new_request.html', context)


@login_required(login_url="accounts:login")
def send_docs(request, slug):

    try:
        requirement = Request.objects.get(slug=slug)
    except Request.DoesNotExist:
        return render(request, 'global/404.html', status='404')
    
    context = {
        'page_settings': {
            'title': 'Envio de documentos',
        },
        'requirement': requirement,

    }
    
    if request.method == "POST":
        rg_frente = request.POST.get('rg-frente')
        rg_verso = request.POST.get('rg-verso')
        cpf = request.POST.get('cpf')
        laudo_frente = request.POST.get('laudo-frente')
        laudo_verso = request.POST.get('laudo-verso')
        compr_res = request.POST.get('comp-res')
        audiometria = None
        if requirement.deficiencia_tipo == "AUD":
            audiometria = request.POST.get('audiometria')
        sangue = request.POST.get('tipo-sangue')
        foto_3x4 = request.POST.get('3x4')



        

    return render(request, 'requerer/send_docs.html', context)
