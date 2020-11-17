from django import forms
from sf.models import Participant
from gtp.models import TeamMember
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class AuthForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


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


class TeamMemberCreateForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['last_name', 'first_name', 'email', 'telegram']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class TeamMemberEditForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"
