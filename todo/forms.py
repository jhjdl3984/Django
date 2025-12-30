from django import forms
from todo.models import TODO, Comment

class TodoForm(forms.ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'description', 'start_date', 'end_date']

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', ]
        label = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3, 'cols': 40, 'class': 'form-control', 'placeholder': '댓글 내용을 입력해주세요.'
            }),
        }




