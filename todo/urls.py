from django.urls import path

from todo.cb_views import TodoListView, TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView

app_name = 'cbv'

urlpatterns = [
    path('todo/', TodoListView.as_view(), name='list'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='info'),
    path('todo/create/', TodoCreateView.as_view(), name='create'),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name='update'),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='delete'),
]