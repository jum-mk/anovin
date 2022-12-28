from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'placeholder': 'Name', 'class': 'form-control', 'style': 'border-radius:8px;'})
        self.fields['subject'].widget.attrs.update(
            {'placeholder': 'Subject', 'class': 'form-control', 'style': 'border-radius:8px;'})
        self.fields['content'].widget.attrs.update(
            {'placeholder': 'Content', 'class': 'form-control', 'style': 'border-radius:8px;'})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'E-mail', 'class': 'form-control', 'style': 'border-radius:8px;'})

    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get("honeypot")
        if honeypot:
            raise forms.ValidationError("This form appears to be a spam submission, so it will not be accepted.")
        return cleaned_data
