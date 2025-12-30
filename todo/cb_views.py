from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from todo.models import TODO, Comment
from todo.forms import CommentForm

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

    # comments => TODO에서 역참조로 Comment들을 가져와라 (Comment 모델의 ForeignKey가 만들어준 역참조 관계 이름)
    # comments__user => comments를 기준으로 그 Comment의 user를 따라가서 User을 가져와라
    # => TODO.objects.all() => 모든 TODO를 가져오고
    #    .prefetch_related('comments' => TODO->Comment 역참조로 각 TODO의 comments들을 미리 가져오고
    #    , 'comments__user') => TODO->Comment->User 관계를 따라가 각 Commnet 객체의 user(FK)까지 미리 가져옴
    queryset = TODO.objects.all().prefetch_related('comments', 'comments__user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)  # => url에서 pk 읽고 -> TODO 모델에서 객체 잦고 -> 결과를 obj에 저장
        
        # obj.user => 해당 TODO(obj)를 작성한 유저
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 To Do를 조회할 권한이 없습니다.')
        return obj
    
    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by('-created_at')
        paginator = Paginator(comments, 5)
        context = {
            'todo': self.object.__dict__,
            'comment_form': CommentForm(),
            'page_obj': paginator.get_page(self.request.GET.get('page')),
            }

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
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = TODO.objects.get(id=self.kwagrs['todo_id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('cbv: info', kwargs={'pk': self.kwargs['todo_id']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        # queryset => Comment.objects.all() => 모든 게시물의 모든 댓글
        # .get_object(queryset) => 전체 댓글 중 url 경로에 있는 pk가 일치하는 하나의 댓글
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 댓글을 수정할 권한이 없습니다.')
        
        return obj
    
    def get_success_url(self):
        return reverse_lazy('cbv:info', kwargs={'pk': self.object.todo.id})
        
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('해당 댓글을 삭제할 권한이 없습니다.')
        
        return obj
    
    def get_success_url(self):
        return reverse_lazy('cbv:list')