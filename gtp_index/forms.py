from django import forms
from .models import Participant


class ParticipantCreateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['last_name', 'first_name', 'email', 'telegram']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class ParticipantEditForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"