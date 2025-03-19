from django.forms import ModelForm, CharField, TextInput, CheckboxSelectMultiple, ModelMultipleChoiceField, \
    SelectMultiple
from .models import Note,Tag


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    existing_tags = ModelMultipleChoiceField(
        queryset=Tag.objects.none(),  # оновимо в __init__
        widget=CheckboxSelectMultiple,
        required=False,
        label="Choose existing tags"
    )
    new_tag = CharField(max_length=150, required=False, label="Add new tag")

    class Meta:
        model = Note
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['existing_tags'].queryset = Tag.objects.filter(user=user)