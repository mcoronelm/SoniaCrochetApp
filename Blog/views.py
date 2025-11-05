from django.shortcuts import render
from .models import Categoria, Post


def blog(request):
    # return HttpResponse("Blog")
    categorias = Categoria.objects.all() #obtiene todas las categorías
    posts = Post.objects.all() #Obtiene todos los post

    return render(request, "blog.html", {"posts": posts, "categorias": categorias})

def categoria(request, categoria_id):
    categoria_obj = Categoria.objects.get(id=categoria_id)
    posts = Post.objects.filter(categorias = categoria_obj)
    return render(request, "categorias.html", {"categoria": categoria_obj, "posts": posts})
