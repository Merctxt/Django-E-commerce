from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 9

class DetalheProdutos(View):
    ...

class AdicionarAoCarrinho(View):
    ...

class RemoverDoCarrinho(View):
    ...

class Carrinho(View):
    ...

class Finalizar(View):
    ...