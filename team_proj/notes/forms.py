# forms.py (in your notes app)
from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    new_tags = forms.CharField(
        max_length=200,
        required=False,
        help_text="Enter new tags, separated by commas.",
    )

    class Meta:
        model = Note
        fields = ['name', 'description', 'tags', 'new_tags']

    def clean_new_tags(self):
        new_tags = self.cleaned_data.get('new_tags')
        if new_tags:
            return [tag.strip() for tag in new_tags.split(',')]
        return []

