from django.db import models


class Cultura(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da cultura")
    largura = models.FloatField(verbose_name="Largura (m)")
    comprimento = models.FloatField(verbose_name="Comprimento (m)")
    ruas = models.PositiveIntegerField(verbose_name="Quantidade de ruas")
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def area(self):
        return self.largura * self.comprimento

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Cultura"
        verbose_name_plural = "Culturas"
