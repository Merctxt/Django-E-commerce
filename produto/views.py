from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from . import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 9

class DetalheProdutos(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
             reverse('produto:lista')
             )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)
        
        variacao = get_object_or_404(
            models.Variacao,
            id=variacao_id
        )
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(self.request, 'Estoque esgotado')
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']
        
        if variacao.id in carrinho:
            quantidade_carrinho = carrinho[variacao.id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x'
                    f' no produto {produto_nome}.')
                quantidade_carrinho = variacao_estoque
                
            carrinho[variacao.id]['quantidade'] = quantidade_carrinho
            carrinho[variacao.id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao.id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho
            
        else:
            carrinho[variacao.id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }
            

        self.request.session.save()
        messages.success(
            self.request,
             f'{produto_nome} {variacao_nome} adicionado ao carrinho'
            f' com sucesso.')
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    ...

class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html')

class Finalizar(View):
    ...