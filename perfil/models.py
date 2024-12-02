from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validacpf import valida_cpf

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, help_text='somente números')
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=2,
        default='SP',
        choices=(
            ('SP', 'São Paulo'),
            ('MG', 'Minas Gerais'),
            ('RJ', 'Rio de Janeiro'),
            ('ES', 'Espirito Santo'),
            ('PR', 'Paraná'),
            ('SC', 'Santa Catarina'),
            ('RS', 'Rio Grande do Sul'),
            ('GO', 'Goiás'),
            ('DF', 'Distrito Federal'),
            ('AC', 'Acre'),
            ('AM', 'Amazonas'),
            ('AP', 'Amapa'),
            ('PA', 'Para'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('TO', 'Tocantins'),
            ('AL', 'Alagoas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('MA', 'Maranhão'),
            ('PI', 'Piauí'),
            ('RN', 'Rio Grande do Norte'),
            ('SE', 'Sergipe'),
            ('PB', 'Paraíba'),
            ('PE', 'Pernambuco'),
        ))
    cep = models.CharField(max_length=8)
    telefone = models.CharField(max_length=11)
    celular = models.CharField(max_length=11)
    email = models.EmailField()

    def __str__(self):
        return f'{self.usuario}'
    
    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf
            

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já cadastrado no sistema'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'CPF inválido'

        if re.search('[^0-9]', self.cep) or len(self.cep) != 8:
            error_messages['cep'] = 'CEP inválido'

        if re.search('[^0-9]', self.telefone):
            error_messages['telefone'] = 'Telefone inválido'

        if re.search('[^0-9]', self.celular):
            error_messages['celular'] = 'Celular inválido'

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'