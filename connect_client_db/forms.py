from django import forms
from .models import ClientDbModel


class ClientDbForm(forms.ModelForm):

    types = [
        'MySQL',
        'MongoDB',
        'PostgreSQL',
    ]
    database_type = forms.ChoiceField(choices=[(x, x) for x in types], label='Database Type')

    class Meta:
        model = ClientDbModel
        fields = [
            'database_name',
            'database_type',
            'usern',
            'passw',
            'host',
            'port',
        ]
