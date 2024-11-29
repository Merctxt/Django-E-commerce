from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=250)
    descricao_curta = models.CharField(max_length=250)
    descricao_longa = models.TextField()
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    slug = models.SlugField(unique=True)
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=(('V', 'Variação'), ('S', 'Simples')), default='V')


    def resize_image(self, image, width):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pil = Image.open(image_full_path)
        original_width, original_height = image_pil.size

        if original_width > width:
            new_height = int((width / original_width) * original_height)
            new_img = image_pil.resize((width, new_height), Image.LANCZOS)
            new_img.save(image_full_path, optimize=True, quality=60)
            print(f'Imagem redimensionada para {width}x{new_height}')
        image_pil.close()
        return
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.imagem:
            self.resize_image(self.imagem, 800)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        