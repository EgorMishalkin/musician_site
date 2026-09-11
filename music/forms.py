from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "email",
            "subject",
            "message",
            "reply_requested",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "имя"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "email"}
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "сообщение",
                    "rows": 5,
                }
            ),
        }