from django import forms
from todo.models import TODO

class TodoForm(forms.ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'description', 'start_date', 'end_date']

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']
