from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Void.models import Produto
import openpyxl
from django.core.files.base import ContentFile
from .forms import ProdutoForm,UploadExcelForm # Supondo que você tenha um formulário Django para o produto

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'lista_produtos.html', {'produtos': produtos})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)  # Inclua request.FILES aqui
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'form_produto.html', {'form': form})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)  # Inclua request.FILES aqui
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'form_produto.html', {'form': form})

def eliminar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.delete()
        return redirect('lista_produtos')
    return render(request, 'confirmar_eliminar.html', {'produto': produto})

def upload_excel_view(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            wb = openpyxl.load_workbook(filename=ContentFile(excel_file.read()))
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                produto = Produto(
                    nome=row[0],
                    descricao=row[1],
                    preco=row[2],
                    stock=row[3],
                    sku=row[4],
                    categoria=row[5],
                    cor=row[6],
                    tamanho=row[7],
                )

                imagem_url = row[8] if len(row) > 9 else None# Ajuste o índice conforme a sua planilha
                if imagem_url:
                    try:
                        response = request.get(imagem_url)
                        img_temp = ContentFile(response.content)
                        produto.imagem.save(f"{row[5]}_image.jpg", img_temp)
                    except Exception as e:
                        print(f"Erro ao baixar a imagem de {imagem_url}: {e}")

                produto.save()

            return redirect('home')
    else:
        form = UploadExcelForm()
    return render (request,'exelform.html', {'form': form})