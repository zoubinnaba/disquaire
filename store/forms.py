from django import forms

from store.models import Contact


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'email',
            'name'
        )
