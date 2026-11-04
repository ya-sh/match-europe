from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email address'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'autocapitalize': 'none'}
        ),
    )


class LanguageSelect(forms.Select):
    """Each language name is written in its own language (RGAA 8.7)."""

    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            option['attrs']['lang'] = value
        return option


class EmployerInvitationForm(LoginForm):
    company_name = forms.CharField(
        label=_('Company name (optional)'),
        help_text=_(
            'Shown in the invitation email and on the acceptance page, so the '
            'employer recognises your invitation. It is not checked.'
        ),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off'}),
    )
    language = forms.ChoiceField(
        label=_('Invitation language'),
        choices=(('fr', 'Français'), ('en', 'English'), ('de', 'Deutsch')),
        widget=LanguageSelect,
    )

    def clean_email(self):
        from .models import User

        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _('An account already exists for this email address.')
            )
        return email
