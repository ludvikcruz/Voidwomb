from django import forms
from Void.models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'stock', 'sku','imagem']

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()