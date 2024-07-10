from django.db import models
from accounts.models import CustomUser
from utils.rands import slugify_new


class Request(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    RACA_COR_CHOICES = [
        ('BR', 'Branca'),
        ('PR', 'Preta'),
        ('PA', 'Parda'),
        ('AM', 'Amarela'),
        ('IN', 'Indígena'),
        ('ND', 'Não Declarada'),
    ]

    SANGUE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    UF_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'),
        ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'),
        ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'),
        ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    CID_CHOICES = [
        ('CID-10', 'CID-10'), ('CID-11', 'CID-11')
    ]

    STATUS_CHOICES = [
        ('Em-analise', 'Em análise'),
        ('Deferido', 'Deferido'),
        ('Indeferido', 'Indeferido'),
        ('Pendente', 'Pendente'),
        ('Agendado', 'Agendado'),
        ('Impresso', 'Impresso'),
    ]

    TIPO_DEFICIENCIA_CHOICES = [
        ('AUD', 'Auditiva'),
        ('AUT', 'Autismo'),
        ('FIS', 'Física'),
        ('INT', 'Intelectual'),
        ('MEN', 'Mental'),
        ('VIS', 'Visual'),
    ]

    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    nome_mae = models.CharField(max_length=255)
    nome_pai = models.CharField(max_length=255, blank=True, null=True)
    rg = models.CharField(max_length=20)
    orgao_emissor = models.CharField(max_length=50)
    uf_rg = models.CharField(max_length=2, choices=UF_CHOICES)
    local_nascimento = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    raca_cor = models.CharField(max_length=2, choices=RACA_COR_CHOICES)
    tipo_sanguineo = models.CharField(max_length=3, choices=SANGUE_CHOICES)
    
    telefone = models.CharField(max_length=15)
    
    deficiencia_tipo_cid = models.CharField(max_length=6, choices=CID_CHOICES)
    deficiencia_cid = models.CharField(max_length=10)
    deficiencia_tipo = models.CharField(max_length=50, choices=TIPO_DEFICIENCIA_CHOICES)
    
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, choices=UF_CHOICES)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    motivo_pendencia = models.TextField(blank=True, null=True)
    data_solicitacao = models.DateField(auto_now_add=True, editable=False)
    data_impressao = models.DateTimeField(blank=True, null=True, editable=False)
    impressa = models.BooleanField(default=False, editable=False)

    analista = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False,
        related_name='requests_as_analista'
    )

    slug = models.SlugField(unique=True)

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='requests_as_user'
    )

    def __str__(self):
        return self.nome_completo
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.nome_completo)
        super().save(*args, **kwargs)
        return super().save(*args, **kwargs)
