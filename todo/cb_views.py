from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy

from todo.models import TODO


class TodoListView(LoginRequiredMixin, ListView):
    queryset = TODO.objects.all()
    template_name = 'todo/todo_list.html'

    # paginate = pagination.paginate_by(page)

    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
            
        # Q = request.GET.get(q=
        #         Q(queryset.title = q) |
        #         Q(queryset.content = q)
        #     )
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        
        return queryset
    
class TodoDetailView(LoginRequiredMixin, DetailView):
    model = TODO
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)  # => url에서 pk 읽고 -> TODO 모델에서 객체 잦고 -> 결과를 obj에 저장
        
        # obj.user => 해당 TODO(obj)를 작성한 유저
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 To Do를 조회할 권한이 없습니다.')
        return obj
    
    def get_context_data(self, **kwargs):
        context = {'todo': self.object.__dict__}

        return context
    
class TodoCreateView(LoginRequiredMixin, CreateView):
    model = TODO
    template_name = 'todo/todo_create.html'
    fields = ['title', 'description', 'start_date', 'end_date']

    def form_valid(self, form):
        # self.object => 생성 요청 폼 데이터
        self.object = form.save(commit=False)

        # self.object.user => 생성 요청 폼 데이터의 user 필드에 요청 user을 넣음
        self.object.user = self.request.user

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        # return HttpResponseRedirect('info')
        return reverse_lazy('cbv:info', kwargs={'pk': self.object.id})
    
class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = TODO
    template_name = 'todo/todo_update.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed', 'id']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('자신의 TODO만 수정할 수 있습니다.')
        return obj
    
    def get_success_url(self):
        return reverse_lazy('cbv:info', kwargs={'pk': self.object.id})
    
class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = TODO

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 To Do를 삭제할 권한이 없습니다.')
        
        return obj
    
    def get_success_url(self):
        return reverse_lazy('cbv:list')