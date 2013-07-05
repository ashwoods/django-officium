

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

try:
    import floppyforms as forms
except ImportError:
    from django import forms

from .models import OfficiumUser
from .conf import settings

attrs_dict = {'class': 'required'}


class OfficiumKwargModelFormMixin(object):
    pass


class HstoreBaseFormMixin(object):
    def save(self, commit=True):

        if self.instance.pk:
            officium_user = self.instance
        else:
            officium_user = OfficiumUser.objects.create(officium=self.officium)

        if self.errors:
            raise ValueError("No form save because of invalid data")

        if commit:
            officium_user.profile_data = self.cleaned_data
            officium_user.save()

            return officium_user
        return self.cleaned_data


class SignupForm(OfficiumKwargModelFormMixin, HstoreBaseFormMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class EditProfileForm(SignupForm):
    pass

def identification_field_factory(label, error_required):
    """
    A simple identification field factory which enable you to set the label.

    :param label:
        String containing the label for this field.

    :param error_required:
        String containing the error message if the field is left empty.

    """
    return forms.CharField(label=label,
                           widget=forms.TextInput(attrs=attrs_dict),
                           max_length=75,
                           error_messages={'required': _("%(error)s") % {'error': error_required}})


class AuthenticationForm(forms.Form):
    """
    A custom form where the identification can be a e-mail address or username.

    """
    identification = identification_field_factory(_(u"Email or username"),
                                                  _(u"Either supply us with your email or username."))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),
                                     required=False,
                                     label=_(u'Remember me for %(days)s') % {'days': _(settings.OFFICIUM_REMEMBER_ME_DAYS[0])})

    def __init__(self, *args, **kwargs):
        """ A custom init because we need to change the label if no usernames is used """
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Dirty hack, somehow the label doesn't get translated without declaring
        # it again here.
        self.fields['remember_me'].label = _(u'Remember me for %(days)s') % {'days': _(settings.OFFICIUM_REMEMBER_ME_DAYS[0])}
        if settings.OFFICIUM_WITHOUT_USERNAMES:
            self.fields['identification'] = identification_field_factory(_(u"Email"),
                                                                         _(u"Please supply your email."))

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            user = authenticate(identification=identification, password=password)
            if user is None:
                raise forms.ValidationError(_(u"Please enter a correct username or email and password. Note that both fields are case-sensitive."))
        return self.cleaned_data
