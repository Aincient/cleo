from django import forms
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'AddNumRequestsForm',
)


class AddNumRequestsForm(forms.Form):
    """Add credits (`num_requests`) form. To be used in admin."""

    num_requests = forms.IntegerField(
        min_value=1,
        required=True,
        label=_("Number of requests")
    )

    class Meta(object):
        """Options."""

        fields = ('num_requests',)
