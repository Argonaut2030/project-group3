from django.forms import ModelForm, CharField, TextInput,CheckboxSelectMultiple,ModelMultipleChoiceField 
from .models import Note,Tag



class NoteForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=CheckboxSelectMultiple())

    class Meta:
        model = Note
        fields = ['name', 'description'] # tags is removed from here

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
