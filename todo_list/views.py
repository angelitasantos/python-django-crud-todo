from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from .models import Todo


def todo_list(request):
    title = 'Listar Tarefas'
    todos = Todo.objects.all().order_by('category', 'description')

    status_filtrar = request.GET.get('status')
    if status_filtrar:
        todos = todos.filter(status = status_filtrar)

    category_filtrar = request.GET.get('category')
    if category_filtrar:
        todos = todos.filter(category = category_filtrar)

    description_filtrar = request.GET.get('description')
    if description_filtrar:
        todos = todos.filter(description__icontains = description_filtrar)

    context =   {   'title': title,
                    'todos': todos}
    return render(request, 'todo_list.html', context)


def todo_create(request):
    title = 'Criar Tarefa'
    if request.method == "GET":
        return redirect('/')
    elif request.method == "POST":
        description = request.POST.get('description')
        category = request.POST.get('category')

        if (len(description.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos !!!')
            return redirect('/')

        todos = Todo.objects.filter(description=description)

        if todos.exists():
            messages.add_message(request, constants.ERROR, 'Existe uma tarefa cadastrada com esta descrição !!!')
            return redirect('/')

        try:
            todo = Todo(    description=description,
                            category=category)
            todo.save()

            todos = Todo.objects.all()
            context =   {   'title': title,
                            'todos': todos}
            messages.add_message(request, constants.SUCCESS, 'Tarefa Incluída com Sucesso!')
            return render(request, 'todo_list.html', context)
        except:
            messages.add_message(request, constants.ERROR, 'Erro Interno do Sistema!!!')
            return redirect('/')


def todo_view(request, id):
    title = 'Editar Tarefa'
    todos = Todo.objects.filter(id=id)

    if not todos.exists():
        messages.add_message(request, constants.ERROR, 'Não existe uma tarefa com este identificador !!!')
        return redirect('/')

    todo = Todo.objects.get(id=id)
    context =   {   'title': title,
                    'todo': todo}
    return render(request, 'todo_update.html', context)


def todo_update(request, id):
    title = 'Alterar Tarefa'

    description = request.POST.get('description')
    category = request.POST.get('category')
    status = request.POST.get('status')

    todo = Todo.objects.get(id=id)
    context =   {   'title': title,
                    'todo': todo}

    if (len(description.strip()) == 0):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos !!!')
        return render(request, 'todo_update.html', context)

    todos = Todo.objects.filter(id=id)
    if todos.exists():
        try:    
            todo.description = description
            todo.category = category
            todo.status = status

            todo.save()

            messages.add_message(request, constants.SUCCESS, 'Tarefa Alterada com Sucesso!')
            return redirect('/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro Interno do Sistema!!!')
            return redirect('/')


def todo_delete(request, id):
    todos = Todo.objects.filter(id=id)

    if not todos.exists():
        messages.add_message(request, constants.ERROR, 'Não existe uma tarefa com este identificador !!!')
        return redirect('/')
    else:
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()
            messages.add_message(request, constants.SUCCESS, 'Tarefa Excluída com Sucesso!')
            return redirect('/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro Interno do Sistema!!!')
            return redirect('/')

