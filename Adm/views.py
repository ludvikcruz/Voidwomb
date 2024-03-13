import csv
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Void.models import Produto
from django.contrib import messages
import openpyxl
from django.core.files.base import ContentFile
from .forms import ProdutoForm,UploadExcelForm 
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator


def lista_produtos(request):
    produtos_list = Produto.objects.all()
    paginator = Paginator(produtos_list, 10) # Mostra 10 produtos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    return render(request, 'lista_produtos.html', {'page_obj': page_obj,'form':form})



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


def login_view(request):
    # Se o user já está logado, redirecioná-lo.
    if request.user.is_authenticated:
        return redirect('admin')
    if request.method == 'POST':
        # Pegar as informações do formulário.
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticar o usuário.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Login bem sucedido") 
            return HttpResponseRedirect(reverse('admin'))
        else:
            # Se a autenticação falhou, retorne algum erro.
            messages.error(request,'Email ou password incorretos.')
            return HttpResponseRedirect(reverse('login'))
        # Método GET, renderize o formulário de login.
    return render(request, 'login.html')
    
def register_view():
    pass

def adm(request):
    
    return render(request,'adm.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def exportar_produtos_csv(request):
    # Criar uma resposta do tipo arquivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos.csv"'

    # Criar um escritor CSV usando a resposta como arquivo
    writer = csv.writer(response,delimiter=';')

    # Escrever o cabeçalho do CSV
    writer.writerow(['ID', 'Nome', 'Descrição', 'Preço', 'Estoque', 'SKU', 'Categoria', 'Cor', 'Tamanho'])

    # Obter os produtos da base de dados
    produtos = Produto.objects.all()

    # Escrever os dados de cada produto
    for produto in produtos:
        writer.writerow([produto.id, produto.nome, produto.descricao, produto.preco, produto.stock, produto.sku, produto.categoria, produto.cor, produto.tamanho])

    # Retornar a resposta que agora contém o arquivo CSV
    return response