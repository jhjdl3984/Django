from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404

from todo.models import TODO
from todo.forms import TodoForm, TodoUpdateForm


@login_required()
def todo_list(request):
    todo_list = TODO.objects.filter(user=request.user).order_by('created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(todo_list, 10)    # 한 페이지당 10개의 TODO를 보여줌
    page_number = request.GET.get('page')

    # get_page(page_number) => 해당 pgae_number의 TODO 10개 묶음을 에러 없이 가져오는 함수
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'todo/todo_list.html', context)

@login_required()
def todo_info(request, todo_id):
    todo = get_object_or_404(TODO, id=todo_id)

    context = {
        'todo': todo.__dict__   # => todo를 dict형태로 (items 메서드 사용 위해)
    }

    return render(request, 'todo/todo_info.html', context)

@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)

    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()

        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    
    context = {
        'form': form
    }

    return render(request, 'todo/todo_create.html', context)

@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(TODO, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)

    if form.is_valid():
        form.save()
        
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))

    context = {
        'form': form
    }

    return render(request, 'todo/todo_update.html', context)

@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(TODO, id=todo_id, user=request.user)
    todo.delete()

    return redirect(reverse('todo_list'))